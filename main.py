import json
import logging
import sys

from lib.core import SixPercent

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    bot = SixPercent()

    # Loads user configurations from users.json
    with open('users.json', 'r') as u:
        user_data = json.load(u)
    # end with

    # Loops through all active users in users.json
    for user in user_data:
        if not user['is_active']:
            continue
        # end if

        logging.info(f"{user['photo']} {user['uid']}")
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

    else:
        sys.exit()
    # end for

# end if
