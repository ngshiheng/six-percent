import logging
import random
import time
from contextlib import suppress

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from lib.constants import (BANK_DROPDOWN_SELECTION_XPATH,
                           ENGLISH_LANGUAGE_BUTTON_XPATH,
                           ERROR_PROMPT_OK_BUTTON_XPATH, FUNDS_XPATH,
                           INVESTMENT_AMOUNT_XPATH,
                           LOGOUT_CONFIRMATION_MESSAGE_XPATH,
                           MAX_PURCHASE_RETRY_ATTEMPTS, PASSWORD_XPATH,
                           PAYMENT_TIMEOUT_LIMIT,
                           PEP_DECLARATION_PROMPT_NEXT_BUTTON_XPATH,
                           PEP_DECLARATION_PROMPT_XPATH, PORTFOLIO_URL_XPATH,
                           PROMPT_OK_BUTTON_XPATH,
                           SECURITY_PHRASE_CONFIRMATION, SUBMIT_BUTTON_XPATH,
                           TERMS_AND_CONDITIONS_CHECKBOX_XPATH, TIMEOUT_LIMIT,
                           TOTAL_FUND_COUNT, USERNAME_XPATH)

logging.basicConfig(level=logging.INFO)


class SixPercent:
    """
    This is a bot which helps to automatically purchase ASNB Fixed Price UT units
    """

    def __init__(self, chrome_driver_path: str, url: str):
        self.url = url
        self.chrome_driver_path = chrome_driver_path

    def idle(self, seconds: float = 0.5) -> None:
        """
        Bot goes to sleep for X seconds
        """
        time.sleep(random.uniform(seconds, seconds * 2))

    def launch_browser(self) -> WebDriver:
        """
        Launches a chromedriver instance in fullscreen
        """
        browser = webdriver.Chrome(self.chrome_driver_path)
        browser.get(self.url)
        browser.maximize_window()
        return browser

    def login(self, browser: WebDriver, asnb_username: str, asnb_password: str) -> None:
        """
        Logs user into the main ASNB portal with their username & password
        """
        wait = WebDriverWait(browser, TIMEOUT_LIMIT)

        username_field = wait.until(EC.element_to_be_clickable((By.XPATH, USERNAME_XPATH)))
        username_field.send_keys(asnb_username)
        username_field.send_keys(Keys.ENTER)

        wait.until(EC.element_to_be_clickable((By.XPATH, SECURITY_PHRASE_CONFIRMATION))).click()  # "Adakah ini frasa keselamatan anda?"

        password_field = wait.until(EC.element_to_be_clickable((By.XPATH, PASSWORD_XPATH)))
        password_field.send_keys(asnb_password)
        password_field.send_keys(Keys.ENTER)

    def logout(self, browser: WebDriver) -> None:
        """
        Logs user out of the main ASNB portal
        """
        wait = WebDriverWait(browser, TIMEOUT_LIMIT)

        try:
            wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "LOGOUT"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, LOGOUT_CONFIRMATION_MESSAGE_XPATH)))
            logging.info('Successfully logged out')

        except Exception as e:
            logging.exception(e)
            raise

        else:
            browser.close()

    def purchase(self, browser: WebDriver, investment_amount: str) -> None:
        """
        Purchase ASNB Fixed Price UT units
        """
        wait = WebDriverWait(browser, TIMEOUT_LIMIT)
        browser.find_element_by_xpath(ENGLISH_LANGUAGE_BUTTON_XPATH).click()  # Always set language to English

        try:

            for i in range(TOTAL_FUND_COUNT):
                # Select fund to purchase
                logging.info("Selecting fund to invest")
                wait.until(EC.presence_of_all_elements_located((By.XPATH, FUNDS_XPATH)))[i].click()

                # Handle cases where the funds are unavailable (i.e. due to distribution of dividends)
                with suppress(TimeoutException):
                    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH, PROMPT_OK_BUTTON_XPATH))).click()

                # Enter investment amount
                logging.info(f"Entering investment amount RM {investment_amount}")
                wait.until(EC.element_to_be_clickable((By.XPATH, INVESTMENT_AMOUNT_XPATH))).send_keys(investment_amount)

                # Select bank of choice
                logging.info("Selecting Maybank2U as payment bank of choice")
                wait.until(EC.element_to_be_clickable((By.XPATH, BANK_DROPDOWN_SELECTION_XPATH))).click()  # TODO: Allow users to select bank of choice from UI

                # Check the terms and condition checkbox
                logging.info("Agreeing to terms and conditions")
                browser.find_element_by_xpath(TERMS_AND_CONDITIONS_CHECKBOX_XPATH).click()

                submit_purchase_button = wait.until(EC.element_to_be_clickable((By.XPATH, SUBMIT_BUTTON_XPATH)))

                for attempt in range(MAX_PURCHASE_RETRY_ATTEMPTS):
                    self.idle()
                    submit_purchase_button.click()

                    # PEP declaration
                    with suppress(NoSuchElementException):
                        browser.find_element_by_xpath(PEP_DECLARATION_PROMPT_XPATH)
                        logging.info('PEP declaration')
                        browser.find_elements_by_xpath(PEP_DECLARATION_PROMPT_NEXT_BUTTON_XPATH)[1].click()

                    try:
                        ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, PROMPT_OK_BUTTON_XPATH)))
                        logging.info(f"The transaction was declined due to insufficient units available - {attempt + 1}")
                        ok_button.click()

                    except (TimeoutException, NoSuchElementException):
                        logging.info('Please proceed to make payment')
                        self.idle(PAYMENT_TIMEOUT_LIMIT)
                        return None

                # Return to main portfolio page
                browser.find_elements_by_xpath(PORTFOLIO_URL_XPATH)[-1].click()

        except (TimeoutException, NoSuchElementException):
            wait.until(EC.element_to_be_clickable((By.XPATH, ERROR_PROMPT_OK_BUTTON_XPATH))).click()
            logging.exception('Unable to purchase fund now')

        finally:
            self.logout(browser)
