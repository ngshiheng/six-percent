from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import sys
import logging
import json

DELAY = 1


def launch_browser():
    PATH_TO_CHROME_DRIVER = "/home/jerryng/chromedriver"
    ASNB_URL = "https://www.myasnb.com.my/uhsessionexpired"
    browser = webdriver.Chrome(PATH_TO_CHROME_DRIVER)
    browser.get(ASNB_URL)
    return browser


def log_in(browser, asnb_username, asnb_password):

    logging.info('🔑 Logging in')
    browser.find_element_by_class_name("btn-login").click()
    browser.find_element_by_id("username").send_keys(asnb_username)
    browser.find_element_by_id("username").send_keys(Keys.ENTER)

    time.sleep(DELAY)
    browser.find_element_by_id("yes").click()
    browser.find_element_by_id("j_password_user").send_keys(asnb_password)
    browser.find_element_by_id("j_password_user").send_keys(Keys.ENTER)
    logging.info('🔓 Successfully logged in')


def log_out(browser):
    time.sleep(DELAY)
    browser.find_element_by_link_text('LOG KELUAR').click()
    logging.info('🔒 Logged out gracefully')
    logging.info('💻 Closing browser in 3 seconds')
    time.sleep(3)
    browser.close()


def main_page(browser):
    browser.maximize_window()
    try:
        browser.find_element_by_link_text('Portfolio').click()

    except:
        if browser.current_url == "https://www.myasnb.com.my/uh/uhlogin/authfail":
            session_uncleared = True
            return session_uncleared

    time.sleep(DELAY)

    try:
        # Click on drop down
        browser.find_element_by_xpath(
            '/html/body/div[3]/div/div[3]/div[9]/form/div/button').click()
    except:
        try:
            browser.find_element_by_xpath(
                "//*[contains(text(), 'MASA PELABURAN TAMAT')]")
            logging.info('⛔️ Investment time closed')
            log_out(browser)
        except NoSuchElementException:
            logging.error(f"❗️ {NoSuchElementException}")

    time.sleep(DELAY)

    browser.find_element_by_class_name('asnb-modal-agree').click()
    time.sleep(DELAY)
    browser.find_element_by_link_text('Portfolio').click()

    logging.info('💲 Buying Amanah Saham Wawasan ')
    browser.find_element_by_id('submit_buy_ASW').click()
    time.sleep(DELAY)

    try:
        browser.find_element_by_id('NEXT').click()

    except NoSuchElementException:
        logging.warning(
            '⛔️ Exceeded maximum attempt, please retry for 5 minutes')
        time.sleep(DELAY)
        browser.find_element_by_xpath(
            "//*[contains(text(), 'Tutup')]").click()
        log_out(browser)


def purchase_unit(browser, investment_amount):

    browser.find_element_by_xpath(
        '/html/body/div[3]/form/div/div[1]/div[4]/label/p').click()
    browser.find_element_by_id('btn-unit-fund').click()

    browser.find_element_by_xpath(
        '/html/body/div[3]/form/div/div[1]/div[2]/div/div/input').send_keys(investment_amount)

    logging.info(f"💸 Starting purchasing loop...")
    for attempt in range(10):

        try:
            browser.find_element_by_xpath(
                '/html/body/div[3]/form/div/div[1]/div[2]/div/div/input').send_keys(Keys.ENTER)
            logging.info(f"🎰 Attempt {attempt+1}")
            time.sleep(DELAY)
        except NoSuchElementException:
            browser.maximize_window()
            logging.error(f"❗️ {NoSuchElementException}")
            continue

        try:
            browser.find_element_by_xpath(
                "//*[contains(text(), 'Transaksi tidak berjaya. Sila hubungi Pusat Khidmat Pelanggan ASNB di talian 03-7730 8899. Kod Rujukan Gagal: 1001')]")
            log_out(browser)

        except NoSuchElementException:
            continue


if __name__ == "__main__":

    logging.getLogger().setLevel(logging.INFO)
    with open('users.json', 'r') as f:
        user_data = json.load(f)

    # Loop through all active user in users.json
    for user in user_data:
        logging.info(f"{user['photo']} Current user: {user['uid']}")
        if not user['is_active']:
            continue

        asnb_username = user['credentials']['username']
        asnb_password = user['credentials']['password']
        investment_amount = user['investment_amount']

        # Main
        browser = launch_browser()
        log_in(browser, asnb_username, asnb_password)
        session_uncleared = main_page(browser)
        if session_uncleared:
            browser.close()
            logging.info('💡 Please remember to logout')
            continue

        purchase_unit(browser, investment_amount)

    sys.exit()
