import logging
import random
import time
from contextlib import suppress

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.locators import LoginPageLocators, PortfolioPageLocators, TransactionPageLocators
from src.settings import MAX_PURCHASE_RETRY_ATTEMPTS, PAYMENT_TIMEOUT_LIMIT, TIMEOUT_LIMIT

logger = logging.getLogger("sixpercent")


class SixPercent:
    """A bot that helps to automatically purchase ASNB Fixed Price UT units"""

    def __init__(self, chrome_driver_path: str, url: str) -> None:
        options = Options()
        options.add_argument("start-maximized")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.url = url
        self.browser = webdriver.Chrome(chrome_driver_path, options=options)
        self.wait = WebDriverWait(self.browser, TIMEOUT_LIMIT)

    def idle(self, seconds: float = 0.5) -> None:
        """Idle for a random time (measured in seconds)

        between, and included, N and 2*N seconds
        """
        time.sleep(random.uniform(seconds, seconds * 2))

    def launch_browser(self) -> None:
        """Launch a chromedriver instance and visit main ASNB portal"""
        self.browser.get(self.url)

    def login(self, asnb_username: str, asnb_password: str) -> None:
        """Log user into the main ASNB portal with their username and password"""
        logger.info(f"Logging in as {asnb_username}")
        username_field = self.wait.until(EC.element_to_be_clickable(LoginPageLocators.USERNAME))
        username_field.send_keys(asnb_username)
        username_field.send_keys(Keys.ENTER)

        self.wait.until(EC.element_to_be_clickable(LoginPageLocators.SECURITY_PHRASE_CONFIRMATION)).click()

        password_field = self.wait.until(EC.element_to_be_clickable(LoginPageLocators.PASSWORD))
        password_field.send_keys(asnb_password)
        password_field.send_keys(Keys.ENTER)

    def logout(self) -> None:
        """Log user out of the main ASNB portal"""
        try:
            self.wait.until(EC.element_to_be_clickable(PortfolioPageLocators.LOGOUT_BUTTON)).click()
            self.wait.until(EC.presence_of_element_located(PortfolioPageLocators.LOGOUT_CONFIRMATION_MESSAGE))
            logger.info('Successfully logged out')

        except Exception as e:
            logger.exception(e)
            raise

        else:
            self.browser.close()

    def purchase(self, investment_amount: str, payment_method: str = 'Maybank2U') -> None:
        """Purchase ASNB Fixed Price UT units"""
        try:
            TOTAL_FUNDS = len(self.wait.until(EC.presence_of_all_elements_located(PortfolioPageLocators.FUNDS)))
            for i in range(TOTAL_FUNDS):
                logger.info("Selecting fund to invest")
                self.wait.until(EC.presence_of_all_elements_located(PortfolioPageLocators.FUNDS))[i].click()

                # Handle cases where the funds are unavailable (e.g. due to distribution of dividends)
                with suppress(TimeoutException):
                    WebDriverWait(self.browser, 3).until(EC.presence_of_element_located(TransactionPageLocators.PROMPT_OK_BUTTON)).click()
                    logger.warning("Skipping fund because fund is unavailable.")
                    continue

                logger.info(f"Entering investment amount RM {investment_amount}")
                self.wait.until(EC.element_to_be_clickable(TransactionPageLocators.INVESTMENT_AMOUNT)).send_keys(investment_amount)

                logger.info(f"Selecting {payment_method} as payment method")
                self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//select[@name='banks']/option[@value='{payment_method}']"))).click()

                logger.debug("Agreeing to terms and conditions")
                self.wait.until(EC.element_to_be_clickable(TransactionPageLocators.TERMS_AND_CONDITIONS_CHECKBOX)).click()

                submit_purchase_button = self.wait.until(EC.element_to_be_clickable(TransactionPageLocators.SUBMIT_BUTTON))

                for attempt in range(MAX_PURCHASE_RETRY_ATTEMPTS):
                    self.idle()
                    submit_purchase_button.click()

                    with suppress(TimeoutException, NoSuchElementException):
                        WebDriverWait(self.browser, 1).until(EC.presence_of_element_located(TransactionPageLocators.PEP_DECLARATION_PROMPT))
                        logger.info('PEP declaration')
                        self.wait.until(EC.presence_of_all_elements_located(TransactionPageLocators.PEP_DECLARATION_PROMPT_NEXT_BUTTON))[-1].click()

                    try:
                        ok_button = self.wait.until(EC.element_to_be_clickable(TransactionPageLocators.PROMPT_OK_BUTTON))
                        logger.info(f"The transaction was declined due to insufficient units available (attempt: {attempt + 1})")
                        ok_button.click()

                    except (TimeoutException, NoSuchElementException):
                        self.browser.maximize_window()
                        logger.info("Please proceed to make payment")
                        self.idle(PAYMENT_TIMEOUT_LIMIT)
                        return

                logger.info("Returning to main portfolio page")
                self.wait.until(EC.presence_of_all_elements_located(TransactionPageLocators.MY_ACCOUNT))[-1].click()

        except (TimeoutException, NoSuchElementException):
            with suppress(Exception):
                self.wait.until(EC.element_to_be_clickable(PortfolioPageLocators.ERROR_PROMPT_OK_BUTTON)).click()
            logger.error("Unable to purchase fund now")

        except Exception as e:
            logger.exception(e)
            raise

        finally:
            self.logout()
