#!/usr/bin/env python
import json
import logging
import os
import sys
import time

import schedule

from lib.constants import ASNB_COOLDOWN_PERIOD, ASNB_LOGIN_URL, CHROME_DRIVER_PATH
from lib.core import SixPercent
from lib.gui import login_gui
from lib.log import log_errors
from lib.utils import decrypt_password

logging.basicConfig(level=logging.INFO)


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """

    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)


@log_errors()
def invest_job(user_credentials: dict) -> None:

    logging.info("🦿 Starting Six Percent Bot")

    bot = SixPercent(
        url=ASNB_LOGIN_URL,
        chrome_driver_path=resource_path(CHROME_DRIVER_PATH),
    )

    logging.info(f"🤑 Logging in as {user_credentials['username']}")
    investment_amount = user_credentials['investment_amount']
    asnb_username = user_credentials['username']
    hashed_asnb_password = user_credentials['password']

    asnb_password = decrypt_password(hashed_asnb_password)

    # Login
    browser = bot.launch_browser()
    if not bot.log_in(browser, asnb_username, asnb_password):
        browser.close()
        logging.info("💡 Are you sure you entered the correct username and password?")
        logging.info("💡 Did you forget to logout somewhere else?")
        logging.info("💡 Please always remember to logout to prevent uncleared session")
        return

    # Updates user.json when login is successful
    with open('user.json', 'w') as u:
        json.dump(user_credentials, u)

    # Main loop
    bot.main_page(browser, investment_amount)
    logging.info(f"🤖 Repeating job after {ASNB_COOLDOWN_PERIOD} minutes")


# Start here
if __name__ == "__main__":
    user_credentials = login_gui()

    # Loads user configuration from user.json
    try:
        if bool(user_credentials) is False:
            with open('user.json', 'r') as u:
                user_credentials = json.load(u)

    except FileNotFoundError:
        logging.error('❓ No user found. Please login as new user')
        sys.exit()

    # Run job once on start
    invest_job(user_credentials)

    # Schedule job every ASNB_COOLDOWN_PERIOD minutes
    schedule.every(ASNB_COOLDOWN_PERIOD).minutes.do(invest_job, user_credentials)

    while True:
        schedule.run_pending()
        time.sleep(1)
