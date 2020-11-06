#!/usr/bin/env python
import logging
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from .constants import ASNB_FUNDS_DATA

logging.getLogger().setLevel(logging.INFO)


class SixPercent:
    """
    This is a bot which helps to automatically purchase ASNB Fixed Price UT units
    """

    def __init__(self, chrome_driver_path, url, browser_width=1600, browser_height=900, min_delay=1, max_delay=1):
        self.url = url
        self.chrome_driver_path = chrome_driver_path
        self.browser_width = browser_width
        self.browser_height = browser_height
        self.min_delay = min_delay
        self.max_delay = max_delay

    # end def

    def wait(self) -> None:
        """
        Introduce a random delay between `min_delay` to `max_delay`
        """

        time.sleep(random.uniform(self.min_delay, self.max_delay))
    # end def

    def launch_browser(self):
        """
        Launches a chromedriver instance
        """

        browser = webdriver.Chrome(self.chrome_driver_path)
        browser.get(self.url)
        browser.set_window_size(self.browser_width, self.browser_height)
        return browser
    # end def

    def log_in(self, browser, asnb_username: str, asnb_password: str) -> bool:
        """
        Logs user into the main ASNB portal with username & password
        """

        self.wait()
        logging.info('🔑 Logging in')
        browser.find_element_by_xpath("//*[@class='btn-login']").click()
        browser.find_element_by_id("username").send_keys(asnb_username)
        browser.find_element_by_id("username").send_keys(Keys.ENTER)

        self.wait()
        browser.find_element_by_id("yes").click()
        browser.find_element_by_id("j_password_user").send_keys(asnb_password)
        browser.find_element_by_id("j_password_user").send_keys(Keys.ENTER)

        if browser.current_url == "https://www.myasnb.com.my/uh/uhlogin/authfail":
            logging.warning('⛔️ Unable to login')
            return False
        else:
            logging.info('🔓 Successfully logged in')
            return True
        # end if

    # end def

    def log_out(self, browser) -> None:
        """
        Logs user out of the main ASNB portal
        """

        self.wait()
        browser.find_element_by_link_text('LOG KELUAR').click()
        logging.info('🔒 Logged out gracefully')
        logging.info('💻 Closing browser in a second')
        self.wait()
        browser.close()
    # end def

    def main_page(self, browser, investment_amount: str):
        """
        Navigates around the main pages logging in
        """

        for i, fund in enumerate(ASNB_FUNDS_DATA.values()):
            if not fund['is_active']:
                continue
            # end if

            fund_id = fund['elements']['id']
            initial_investment_xpath = fund['elements']['initial_investment_xpath']

            logging.info(f"💲 Attempting to buy {fund['name']} ({fund['alt_name']})")

            try:
                # Navigate to 'Produk' page
                self.wait()
                browser.find_element_by_link_text('Produk').click()

                # Click 'Transaksi' drop down
                browser.find_element_by_xpath('//div[@class="faq-title1 accordionTitle glyphicon glyphicon-plus-sign"]').click()

            except NoSuchElementException:
                logging.warning(f"⛔️ Unexpected error while attempting to purchase {fund['name']} ({fund['alt_name']})")
                continue
            # end try

            # Figure out if the current attempt is an initial/additional investment
            try:
                self.wait()
                browser.find_element_by_xpath(initial_investment_xpath).click()
                logging.info("🤑 Initial Investment")

            except NoSuchElementException:

                try:
                    self.wait()
                    browser.find_elements_by_class_name("btn.btn-form-submit.btnsbmt.dropdown-toggle")[i].click()
                    self.wait()
                    browser.find_element_by_id(fund_id).click()
                    logging.info("💵 Additional Investment")

                except IndexError:
                    logging.warning(f"⛔️ {fund['name']} ({fund['alt_name']}) is currently unavailable for purchase")
                    continue
                # end try
            # end try

            try:
                # PEP declaration
                logging.info('📜 PEP declaration')
                self.wait()
                browser.find_element_by_id('NEXT').click()

            except NoSuchElementException:

                try:
                    browser.find_element_by_xpath("//*[contains(text(), 'Tutup')]").click()
                    logging.error('⛔️ Exceeded maximum attempt, please retry for 5 minutes')
                    continue
                except Exception:
                    logging.warning('💬 You do not need to declare PEP again')
                    pass
                # end try
            # end try

            # Start purchasing loop
            logging.info(f"💸 Start purchasing loop for {fund['alt_name']}...")
            self.purchase_unit(browser, investment_amount)

        # End of loop
        self.log_out(browser)
    # end def

    def purchase_unit(self, browser, investment_amount: str):
        """
        Attempts to purchase ASNB unit after declaration
        """
        browser.find_element_by_xpath('/html/body/div[3]/form/div/div[1]/div[4]/label/p').click()
        browser.find_element_by_id('btn-unit-fund').click()
        self.wait()
        browser.find_element_by_xpath("//input[@placeholder='0.00']").send_keys(investment_amount)
        browser.find_element_by_xpath("//input[@placeholder='0.00']").send_keys(Keys.ENTER)

        # NOTE: Currently ASNB only allows a maximum of 10 tries per fund
        MAXIMUM_ATTEMPTS = 10

        for attempt in range(MAXIMUM_ATTEMPTS):
            try:
                browser.find_element_by_xpath("//input[@placeholder='0.00']").send_keys(Keys.ENTER)
                logging.info(f"🎰 Attempt {attempt+1}")
                self.wait()
            except NoSuchElementException:
                browser.maximize_window()
                browser.set_window_position(0, 0)
                logging.info("🥳 Success! Please make your payment within the next 5 minutes")
                time.sleep(300)
            # end try

            try:
                browser.find_element_by_xpath("//*[contains(text(), 'Transaksi tidak berjaya. Sila hubungi Pusat Khidmat Pelanggan ASNB di talian 03-7730 8899. Kod Rujukan Gagal: 1001')]")
                browser.find_element_by_xpath('/html/body/div[3]/form/div/div[1]/div[2]/div/div/input').send_keys(Keys.ENTER)
                return

            except NoSuchElementException:
                continue
            # end try

        else:
            logging.info("🔚 End of loop")
        # end for

    # end def

# end class
