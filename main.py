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
def invest_job():

    bot = SixPercent(
        url=config.get('website', 'url'),
        chrome_driver_path=resource_path(config.get('chromedriver', 'path')),
        browser_width=config.getint('browser', 'width'),
        browser_height=config.getint('browser', 'height'),
        min_delay=config.getfloat('delay', 'min_seconds'),
        max_delay=config.getfloat('delay', 'max_seconds'),
    )

    # Loads user configuration from users.json
    with open('users.json', 'r') as u:
        users_data = json.load(u)
    # end with

    # Loops through all active users in users.json
    for user in users_data:
        if user['is_active']:
            logging.info(f"{user['name']}")
            asnb_username = user['credentials']['username']
            asnb_password = user['credentials']['password']
            investment_amount = user['investment_amount']

            # Login
            browser = bot.launch_browser()
            if bot.log_in(browser, asnb_username, asnb_password):
                browser.close()
                logging.info('💡 Did you forget to logout somewhere else?')
                logging.info('💡 Please always remember to logout to prevent uncleared session')
                continue
            # end if

            # Main loop
            bot.main_page(browser, investment_amount)
        # end if
    # end for

# end def


# Start here
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    # Run job once on start
    invest_job()

    # Schedule job every 5 minutes
    schedule.every(config.getint('schedule', 'minutes')).minutes.do(invest_job)

    while True:
        schedule.run_pending()
        time.sleep(1)
    # end while
# end if
