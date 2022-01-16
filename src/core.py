import logging
import random
import time
from contextlib import suppress

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.constants import MAX_PURCHASE_RETRY_ATTEMPTS, PAYMENT_TIMEOUT_LIMIT, TIMEOUT_LIMIT, TOTAL_FUND_COUNT
from src.utils.locators import LoginPageLocators, PortfolioPageLocators, TransactionPageLocators

logging.basicConfig(level=logging.INFO)


class SixPercent:
    """
    This is a bot which helps to automatically purchase ASNB Fixed Price UT units
    """

    def __init__(self, chrome_driver_path: str, url: str) -> None:
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.url = url
        self.browser = webdriver.Chrome(chrome_driver_path, options=options)
        self.wait = WebDriverWait(self.browser, TIMEOUT_LIMIT)

    def idle(self, seconds: float = 0.5) -> None:
        """
        Bot goes to sleep for X seconds
        """
        time.sleep(random.uniform(seconds, seconds * 2))

    def launch_browser(self) -> None:
        """
        Launches a chromedriver instance in fullscreen
        """
        self.browser.get(self.url)
        self.browser.maximize_window()

    def login(self, asnb_username: str, asnb_password: str) -> None:
        """
        Logs user into the main ASNB portal with their username & password
        """

        username_field = self.wait.until(EC.element_to_be_clickable(LoginPageLocators.USERNAME))
        username_field.send_keys(asnb_username)
        username_field.send_keys(Keys.ENTER)

        self.wait.until(EC.element_to_be_clickable(LoginPageLocators.SECURITY_PHRASE_CONFIRMATION)).click()  # "Adakah ini frasa keselamatan anda?"

        password_field = self.wait.until(EC.element_to_be_clickable(LoginPageLocators.PASSWORD))
        password_field.send_keys(asnb_password)
        password_field.send_keys(Keys.ENTER)

    def logout(self) -> None:
        """
        Logs user out of the main ASNB portal
        """
        try:
            self.wait.until(EC.element_to_be_clickable(PortfolioPageLocators.LOGOUT_BUTTON)).click()
            self.wait.until(EC.presence_of_element_located(PortfolioPageLocators.LOGOUT_CONFIRMATION_MESSAGE))
            logging.info('Successfully logged out')

        except Exception as e:
            logging.exception(e)
            raise

        else:
            self.browser.close()

    def purchase(self, investment_amount: str) -> None:
        """
        Purchase ASNB Fixed Price UT units
        """
        try:
            for i in range(TOTAL_FUND_COUNT):
                # Select fund to purchase
                logging.info("Selecting fund to invest")
                self.wait.until(EC.presence_of_all_elements_located(PortfolioPageLocators.FUNDS))[i].click()

                # Handle cases where the funds are unavailable (i.e. due to distribution of dividends)
                with suppress(TimeoutException):
                    WebDriverWait(self.browser, 3).until(EC.presence_of_element_located(TransactionPageLocators.PROMPT_OK_BUTTON)).click()

                # Enter investment amount
                logging.info(f"Entering investment amount RM {investment_amount}")
                self.wait.until(EC.element_to_be_clickable(TransactionPageLocators.INVESTMENT_AMOUNT)).send_keys(investment_amount)

                # Select bank of choice
                logging.info("Selecting Maybank2U as payment bank of choice")
                self.wait.until(EC.element_to_be_clickable(TransactionPageLocators.BANK_DROPDOWN_SELECTION)).click()  # TODO: Allow users to select bank of choice from UI

                # Check the terms and condition checkbox
                logging.info("Agreeing to terms and conditions")
                self.browser.find_element_by_xpath(TransactionPageLocators.TERMS_AND_CONDITIONS_CHECKBOX[1]).click()

                submit_purchase_button = self.wait.until(EC.element_to_be_clickable(TransactionPageLocators.SUBMIT_BUTTON))

                for attempt in range(MAX_PURCHASE_RETRY_ATTEMPTS):
                    self.idle()
                    submit_purchase_button.click()

                    # PEP declaration
                    with suppress(NoSuchElementException):
                        self.browser.find_element_by_xpath(TransactionPageLocators.PEP_DECLARATION_PROMPT[1])
                        logging.info('PEP declaration')
                        self.browser.find_elements_by_xpath(TransactionPageLocators.PEP_DECLARATION_PROMPT_NEXT_BUTTON[1])[1].click()

                    try:
                        ok_button = self.wait.until(EC.element_to_be_clickable(TransactionPageLocators.PROMPT_OK_BUTTON))
                        logging.info(f"The transaction was declined due to insufficient units available - {attempt + 1}")
                        ok_button.click()

                    except (TimeoutException, NoSuchElementException):
                        self.browser.maximize_window()
                        logging.info('Please proceed to make payment')
                        self.idle(PAYMENT_TIMEOUT_LIMIT)
                        return None

                # Return to main portfolio page
                self.browser.find_elements_by_xpath(TransactionPageLocators.PORTFOLIO_URL[1])[-1].click()

        except (TimeoutException, NoSuchElementException):
            self.wait.until(EC.element_to_be_clickable(PortfolioPageLocators.ERROR_PROMPT_OK_BUTTON)).click()
            logging.exception('Unable to purchase fund now')

        finally:
            self.logout()
