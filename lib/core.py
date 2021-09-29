import logging
import time
from contextlib import suppress

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from lib.constants import MAX_PURCHASE_RETRY_ATTEMPTS, TIMEOUT_LIMIT, TOTAL_FUND_COUNT

logger = logging.getLogger(__name__)


class SixPercent:
    """
    This is a bot which helps to automatically purchase ASNB Fixed Price UT units
    """

    def __init__(self, chrome_driver_path: str, url: str):
        self.url = url
        self.chrome_driver_path = chrome_driver_path

    def launch_browser(self) -> WebDriver:
        """
        Launches a chromedriver instance in fullscreen
        """
        browser = webdriver.Chrome(self.chrome_driver_path)
        browser.get(self.url)
        browser.maximize_window()
        return browser

    def login(self, browser: WebDriver, asnb_username: str, asnb_password: str) -> bool:
        """
        Logs user into the main ASNB portal with their username & password
        """
        wait = WebDriverWait(browser, TIMEOUT_LIMIT)

        try:
            username_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']")))
            username_field.send_keys(asnb_username)
            username_field.send_keys(Keys.ENTER)

            wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@id='btnYes']"))).click()  # "Adakah ini frasa keselamatan anda?"

            password_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']")))
            password_field.send_keys(asnb_password)
            password_field.send_keys(Keys.ENTER)

            logger.info('Successfully logged in')
            return True

        except TimeoutException:
            logger.exception('Login attempt failed')
            return False

    def logout(self, browser: WebDriver) -> None:
        """
        Logs user out of the main ASNB portal
        """
        wait = WebDriverWait(browser, TIMEOUT_LIMIT)

        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "LOGOUT"))).click()
        logger.info('Successfully logged out')
        browser.close()

    def main_page(self, browser: WebDriver, investment_amount: str) -> None:
        """
        Navigates around the main pages after login
        """
        FUNDS_XPATH = '//div[@class="bg-white mb-3 w-full mx-auto text-gray-500 grid grid-cols-4 md:grid-cols-5 xl:grid-cols-6 justify-between rounded-lg px-0 py-4 shadow-lg dark:bg-gray-700 dark:text-gray-400 lg:h-48"]'

        wait = WebDriverWait(browser, 2)
        for i in range(TOTAL_FUND_COUNT):
            WebDriverWait(browser, TIMEOUT_LIMIT).until(EC.presence_of_all_elements_located((By.XPATH, FUNDS_XPATH)))[i].click()

            with suppress(TimeoutException):
                wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'not available')]")))
                browser.find_element_by_xpath("//button[contains(text(), 'OK')]").click()
                continue

            amount_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='amount']")))
            amount_field.send_keys(investment_amount)

            wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='banks']/option[@value='Maybank2U']"))).click()  # TODO: Allow users to select bank of choice from UI
            browser.find_element_by_xpath("//input[@type='checkbox']").click()

            submit_purchase_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))

            for _ in range(MAX_PURCHASE_RETRY_ATTEMPTS):
                submit_purchase_button.click()

                # PEP declaration
                with suppress(NoSuchElementException):
                    browser.find_element_by_xpath("//h3[contains(text(), 'Declaration of PEP')]")
                    logger.info('PEP declaration')
                    browser.find_elements_by_xpath("//button[contains(text(), 'Next')]")[1].click()

                # Stop trying when blocked
                with suppress(TimeoutException):
                    wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Blocked')]")))
                    browser.find_element_by_xpath("//button[contains(text(), 'OK')]").click()
                    break

                try:
                    wait.until(EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'insufficient units')]")))
                    logger.info('The transaction was declined due to insufficient units available')
                    browser.find_element_by_xpath("//button[contains(text(), 'OK')]").click()

                except TimeoutException:
                    logger.info('Please proceed to make payment')
                    time.sleep(300)
                    return None

            browser.find_elements_by_xpath("//a[@href='/portfolio']")[1].click()
            continue
