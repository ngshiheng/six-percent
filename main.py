#!/usr/bin/env python
import functools
import json
import logging
import os
import sys
import time
from configparser import ConfigParser

import schedule

from lib.core import SixPercent
from lib.gui import login_gui

# Read user configuration from `config.ini` file
config = ConfigParser()
config.read('config.ini')


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
        logging.info(f"🤖 Repeating job '{func.__name__}' after {config.getint('schedule', 'minutes')} minutes")
        return result
    # end def

    return wrapper
# end def


@with_logging
def invest_job(user_credentials: dict) -> None:

    bot = SixPercent(
        url=config.get('website', 'url'),
        chrome_driver_path=resource_path(config.get('chromedriver', 'path')),
        browser_width=config.getint('browser', 'width'),
        browser_height=config.getint('browser', 'height'),
        min_delay=config.getfloat('delay', 'min_seconds'),
        max_delay=config.getfloat('delay', 'max_seconds'),
    )

    logging.info(f"🤑 Logging in as {user_credentials['username']}")
    asnb_username = user_credentials['username']
    asnb_password = user_credentials['password']
    investment_amount = user_credentials['investment_amount']

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
        #end if

    except FileNotFoundError:
        logging.warning('❓ No user found. Please login as new user')
        sys.exit()
    #end try

    # Run job once on start
    invest_job(user_credentials)

    # Schedule job every 5 minutes
    schedule.every(config.getint('schedule', 'minutes')).minutes.do(invest_job, user_credentials)

    while True:
        schedule.run_pending()
        time.sleep(1)
    # end while
# end if
