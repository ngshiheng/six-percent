#!/usr/bin/env python
import functools
import json
import logging
import os
import sys
import time

import schedule

from lib.constants import ASNB_LOGIN_URL, CHROME_DRIVER_PATH
from lib.core import SixPercent
from lib.gui import login_gui
from lib.utils import decrypt_password


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.dirname(__file__)
    # end try

    return os.path.join(base_path, relative_path)
# end def


def with_logging(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"🦿 Running job '{func.__name__}'")
        result = func(*args, **kwargs)
        logging.info(f"🦾 Job '{func.__name__}' completed")
        logging.info(f"🤖 Repeating job '{func.__name__}' after 5 minutes")
        return result
    # end def

    return wrapper
# end def


@with_logging
def invest_job(user_credentials: dict) -> None:

    bot = SixPercent(
        url=ASNB_LOGIN_URL,
        chrome_driver_path=resource_path(CHROME_DRIVER_PATH),
        min_delay=1,
        max_delay=1.25,
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
        logging.info('💡 Are you sure you entered the correct username and password?')
        logging.info('💡 Did you forget to logout somewhere else?')
        logging.info('💡 Please always remember to logout to prevent uncleared session')
    # end if

    # Updates user.json is login is successful
    with open('user.json', 'w') as u:
        json.dump(user_credentials, u)
    # end with

    # Main loop
    bot.main_page(browser, investment_amount)

# end def


# Start here
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    user_credentials = login_gui()

    # Loads user configuration from user.json
    try:
        if bool(user_credentials) is False:
            with open('user.json', 'r') as u:
                user_credentials = json.load(u)
            # end with
        # end if

    except FileNotFoundError:
        logging.warning('❓ No user found. Please login as new user')
        sys.exit()
    # end try

    # Run job once on start
    invest_job(user_credentials)

    # Schedule job every 5 minutes
    schedule.every(5).minutes.do(invest_job, user_credentials)

    while True:
        schedule.run_pending()
        time.sleep(1)
    # end while
# end if
