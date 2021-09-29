import logging
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from lib.constants import ASNB_FUNDS_DATA

logging.basicConfig(level=logging.INFO)


class SixPercent:
    """
    This is a bot which helps to automatically purchase ASNB Fixed Price UT units
    """

    def __init__(self, chrome_driver_path: str, url: str, min_delay: float = 1.00, max_delay: float = 1.25):
        self.url = url
        self.chrome_driver_path = chrome_driver_path
        self.min_delay = min_delay
        self.max_delay = max_delay

    def _wait(self) -> None:
        """
        Introduce a random delay between `min_delay` to `max_delay`
        """
        time.sleep(random.uniform(self.min_delay, self.max_delay))

    def launch_browser(self) -> WebDriver:
        """
        Launches a chromedriver instance
        """
        browser = webdriver.Chrome(self.chrome_driver_path)
        browser.get(self.url)
        browser.maximize_window()
        return browser

    def log_in(self, browser: WebDriver, asnb_username: str, asnb_password: str) -> bool:
        """
        Logs user into the main ASNB portal with username & password
        """

        try:
            self._wait()
            logging.info('🔑 Logging in')
            browser.find_element_by_xpath("//*[@class='btn-login']").click()
            browser.find_element_by_id("username").send_keys(asnb_username)
            browser.find_element_by_id("username").send_keys(Keys.ENTER)

            self._wait()
            browser.find_element_by_id("yes").click()
            browser.find_element_by_id("j_password_user").send_keys(asnb_password)
            browser.find_element_by_id("j_password_user").send_keys(Keys.ENTER)

            logging.info('🔓 Successfully logged in')
            return True

        except NoSuchElementException:
            logging.exception('⛔️ Unable to login')
            return False

    def log_out(self, browser: WebDriver) -> None:
        """
        Logs user out of the main ASNB portal
        """
        self._wait()
        browser.find_element_by_link_text('LOG KELUAR').click()
        logging.info('🔒 Logged out gracefully')
        logging.info('💻 Closing browser in a second')
        self._wait()
        browser.close()

    def main_page(self, browser: WebDriver, investment_amount: str) -> None:
        """
        Navigates around the main pages after logging in
        """
        order = 0  # NOTE: This is use to handle case where ASM is not available. The order of the drop-down elements does not always correspond to the availability of the funds
        for fund in ASNB_FUNDS_DATA.values():
            if not fund['is_active']:
                continue

            fund_id = fund['elements']['id']
            initial_investment_xpath = fund['elements']['initial_investment_xpath']

            logging.info(f"💲 Attempting to buy {fund['name']} ({fund['alt_name']})")

            try:
                # Navigate to 'Produk' page
                self._wait()
                browser.find_element_by_link_text('Produk').click()

                # Click 'Transaksi' drop down
                browser.find_element_by_xpath('//div[@class="faq-title1 accordionTitle glyphicon glyphicon-plus-sign"]').click()

            except NoSuchElementException:

                logging.exception(f"⛔️ Unexpected error while attempting to purchase {fund['name']} ({fund['alt_name']})")
                continue

            # Figure out if the current attempt is an initial/additional investment
            try:
                self._wait()
                browser.find_element_by_xpath(initial_investment_xpath).click()
                logging.info("🤑 Initial Investment")

            except NoSuchElementException:

                try:
                    self._wait()
                    browser.find_elements_by_class_name("btn.btn-form-submit.btnsbmt.dropdown-toggle")[order].click()
                    self._wait()
                    browser.find_element_by_id(fund_id).click()
                    logging.info("💵 Additional Investment")

                except (IndexError, NoSuchElementException):
                    logging.warning(f"⛔️ {fund['name']} ({fund['alt_name']}) is currently unavailable for purchase")
                    continue

            order += 1  # NOTE: We only increment this whenever the fund is available for purchase, i.e. it has drop-down
            try:
                # PEP declaration
                logging.info('📜 PEP declaration')
                self._wait()
                browser.find_element_by_id('NEXT').click()

            except NoSuchElementException:

                try:
                    browser.find_element_by_xpath("//*[contains(text(), 'Tutup')]").click()
                    logging.error('⛔️ Exceeded maximum attempt, please retry for 5 minutes')
                    continue
                except Exception:
                    logging.info('💬 You do not need to declare PEP again')

            # Start purchasing loop
            logging.info(f"💸 Start purchasing loop for {fund['alt_name']}...")
            self._purchase_unit(browser, investment_amount)

        # End of loop
        return self.log_out(browser)

    def _purchase_unit(self, browser: WebDriver, investment_amount: str) -> None:
        """
        Attempts to purchase ASNB unit after declaration
        """
        browser.find_element_by_xpath("//*[contains(text(), 'Saya telah membaca, memahami dan bersetuju dengan kenyataan')]").click()
        browser.find_element_by_id('btn-unit-fund').click()
        self._wait()
        browser.find_element_by_xpath("//input[@placeholder='0.00']").send_keys(investment_amount)
        browser.find_element_by_xpath("//input[@placeholder='0.00']").send_keys(Keys.ENTER)

        # NOTE: Currently ASNB only allows a maximum of 10 tries per fund
        MAXIMUM_ATTEMPTS = 10

        for attempt in range(MAXIMUM_ATTEMPTS):
            try:
                browser.find_element_by_xpath("//input[@placeholder='0.00']").send_keys(Keys.ENTER)
                logging.info(f"🎰 Attempt {attempt+1}")
                self._wait()

            except NoSuchElementException:
                browser.maximize_window()
                browser.set_window_position(0, 0)
                logging.info("🥳 Success! Please make your payment within the next 5 minutes")

                # To ensure user has enough time to make payment
                time.sleep(300)  # seconds

            try:
                browser.find_element_by_xpath("//*[contains(text(), 'Transaksi tidak berjaya. Sila hubungi Pusat Khidmat Pelanggan ASNB di talian 03-7730 8899. Kod Rujukan Gagal: 1001')]")
                browser.find_element_by_id('btn-unit-fund').send_keys(Keys.ENTER)
                return

            except NoSuchElementException:
                continue

        else:
            logging.info("🔚 End of loop")
