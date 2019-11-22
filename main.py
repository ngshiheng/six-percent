from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
import sys
import logging
import json

DELAY = 1


def launch_browser():
    # Start Chrome browser
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

    # Maximize browser window
    browser.maximize_window()

    # Navigate to portfolio page
    try:
        browser.find_element_by_link_text('Portfolio').click()

    except:
        logging.info('⛔️ User has uncleared session')
        if browser.current_url == "https://www.myasnb.com.my/uh/uhlogin/authfail":
            return True

    time.sleep(DELAY)


def log_out(browser):
    time.sleep(DELAY)
    browser.find_element_by_link_text('LOG KELUAR').click()
    logging.info('🔒 Logged out gracefully')
    logging.info('💻 Closing browser in 3 seconds')
    time.sleep(3)
    browser.close()


def main_page(browser, investment_amount):

    with open('funds.json', 'r') as f:
        fund_data = json.load(f)

    for fund in fund_data:
        if not fund['is_active']:
            continue

        logging.info(
            f"💲 Attempting to buy {fund['name']} ({fund['alternate_name']})")

        fund_xpath = fund['elements']['drop_down_xpath']
        fund_id = fund['elements']['id']

        try:
            # Click on drop down
            time.sleep(DELAY)
            browser.find_element_by_xpath(fund_xpath).click()
            browser.find_element_by_id(fund_id).click()
        except:
            try:
                browser.find_element_by_xpath(
                    "//*[contains(text(), 'MASA PELABURAN TAMAT')]")
                logging.info('⛔️ Investment time closed')
                log_out(browser)
            except NoSuchElementException:
                logging.warning(
                    '⛔️ Unexpected error')
            continue

        time.sleep(DELAY)

        try:
            # PEP declaration
            logging.info(
                '📜 PEP declaration')
            browser.find_element_by_id('NEXT').click()

        except NoSuchElementException:

            # time.sleep(DELAY)
            try:
                browser.find_element_by_xpath(
                    "//*[contains(text(), 'Tutup')]").click()
                logging.warning(
                    '⛔️ Exceeded maximum attempt, please retry for 5 minutes')
                continue
            except:
                logging.warning(
                    '💬 You do not need to declare PEP again')
                pass

        # Start purchasing loop
        logging.info(
            f"💸 Start purchasing loop for {fund['alternate_name']}...")
        purchase_unit(browser, investment_amount)

    # End of loop
    logging.info(f"💸 End of loop...")
    log_out(browser)


def purchase_unit(browser, investment_amount):
    browser.find_element_by_xpath(
        '/html/body/div[3]/form/div/div[1]/div[4]/label/p').click()
    browser.find_element_by_id('btn-unit-fund').click()

    browser.find_element_by_xpath(
        '/html/body/div[3]/form/div/div[1]/div[2]/div/div/input').send_keys(investment_amount)

    for attempt in range(10):

        try:
            browser.find_element_by_xpath(
                '/html/body/div[3]/form/div/div[1]/div[2]/div/div/input').send_keys(Keys.ENTER)
            logging.info(f"🎰 Attempt {attempt+1}")
            time.sleep(DELAY)
        except NoSuchElementException:
            browser.maximize_window()
            logging.error(
                f"🥳 Success! Please make your payment within the next 5 minutes")
            time.sleep(300)

        try:
            browser.find_element_by_xpath(
                "//*[contains(text(), 'Transaksi tidak berjaya. Sila hubungi Pusat Khidmat Pelanggan ASNB di talian 03-7730 8899. Kod Rujukan Gagal: 1001')]")
            browser.find_element_by_xpath(
                '/html/body/div[3]/form/div/div[1]/div[2]/div/div/input').send_keys(Keys.ENTER)
            return

        except NoSuchElementException:
            continue


if __name__ == "__main__":

    logging.getLogger().setLevel(logging.INFO)

    # Loads user info
    with open('users.json', 'r') as u:
        user_data = json.load(u)

    # Loop through all active user in users.json
    for user in user_data:
        if not user['is_active']:
            continue
        logging.info(f"{user['photo']} {user['uid']}")
        asnb_username = user['credentials']['username']
        asnb_password = user['credentials']['password']
        investment_amount = user['investment_amount']

        # Main
        browser = launch_browser()
        if log_in(browser, asnb_username, asnb_password):
            browser.close()
            logging.info('💡 Did you forget to logout somewhere else?')
            logging.info(
                '💡 Please always remember to logout to prevent uncleared session')
            continue

        main_page(browser, investment_amount)

    sys.exit()
