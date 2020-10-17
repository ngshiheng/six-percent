#!/usr/bin/env python

import json
import logging
import sys
import time
from configparser import ConfigParser

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

logging.getLogger().setLevel(logging.INFO)


class SixPercent:
    """
    This is a bot which helps to automatically purchase ASNB Fixed Price UT units
    """

    def __init__(self):

        # Read user configurations from `config.ini` file
        config = ConfigParser()
        config.read('config.ini')

        self.PATH_TO_CHROME_DRIVER = config.get('chromedriver', 'path')
        self.ASNB_URL = config.get('website', 'url')
        self.BROWSER_WIDTH = config.get('browser', 'width')
        self.BROWSER_HEIGHT = config.get('browser', 'height')

    # end def

    def wait(self, delay=1):
        """
        Delay method, in seconds
        """
        time.sleep(delay)
    # end def

    def launch_browser(self):
        """
        Launches a chromedriver instance
        """

        browser = webdriver.Chrome(self.PATH_TO_CHROME_DRIVER)
        browser.get(self.ASNB_URL)

        return browser

    # end def

    def log_in(self, browser, asnb_username, asnb_password):
        """
        Logs user into the main ASNB portal with username & password
        """

        logging.info('🔑 Logging in')
        browser.find_element_by_class_name("btn-login").click()
        browser.find_element_by_id("username").send_keys(asnb_username)
        browser.find_element_by_id("username").send_keys(Keys.ENTER)

        self.wait()
        browser.find_element_by_id("yes").click()
        browser.find_element_by_id("j_password_user").send_keys(asnb_password)
        browser.find_element_by_id("j_password_user").send_keys(Keys.ENTER)
        logging.info('🔓 Successfully logged in')

        browser.set_window_size(self.BROWSER_WIDTH, self.BROWSER_HEIGHT)
    # end def

    def log_out(self, browser):
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

    def main_page(self, browser, investment_amount):
        """
        Navigates around the main pages logging in
        """

        with open('funds.json', 'r') as f:  # TODO: set this in a configuration file
            fund_data = json.load(f)

        for i, fund in enumerate(fund_data):
            if fund['skip']:
                continue
            # end if

            fund_id = fund['elements']['id']
            initial_investment_xpath = fund['elements']['initial_investment_xpath']

            logging.info(f"💲 Attempting to buy {fund['name']} ({fund['alternate_name']})")

            try:
                # Navigate to 'Produk' page
                browser.find_element_by_link_text('Produk').click()

                # Click 'Transaksi' drop down
                browser.find_element_by_xpath('//div[@class="faq-title1 accordionTitle glyphicon glyphicon-plus-sign"]').click()

            except NoSuchElementException:
                logging.warning('⛔️ User has uncleared session')
                return True if browser.current_url == "https://www.myasnb.com.my/uh/uhlogin/authfail" else False
            # end try

            self.wait()

            try:
                browser.find_elements_by_class_name("btn.btn-form-submit.btnsbmt.dropdown-toggle")[i].click()

            except IndexError:
                logging.warning(f"⛔️ {fund['name']} ({fund['alternate_name']}) is currently unavailable for purchase")
                continue
            # end try

            try:
                # Figure out if the current attempt is an initial/additional investment
                try:
                    self.wait()
                    browser.find_element_by_xpath(initial_investment_xpath).click()
                    logging.info("🤑 Initial Investment")

                except NoSuchElementException:
                    self.wait()
                    browser.find_element_by_id(fund_id).click()
                    logging.info("💵 Additional Investment")
                # end try

            except NoSuchElementException:
                try:
                    browser.find_element_by_xpath("//*[contains(text(), 'MASA PELABURAN TAMAT')]")
                    logging.error('⛔️ Investment time closed')
                    self.log_out(browser)
                    sys.exit()

                except NoSuchElementException:
                    logging.error(f"⛔️ Unexpected error while attempting to purchase {fund['name']} ({fund['alternate_name']})")
                    self.log_out(browser)
                    sys.exit()
                # end try
            # end try

            self.wait()
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
            logging.info(f"💸 Start purchasing loop for {fund['alternate_name']}...")
            self.purchase_unit(browser, investment_amount)

        # End of loop
        self.log_out(browser)
    # end def

    def purchase_unit(self, browser, investment_amount):
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
