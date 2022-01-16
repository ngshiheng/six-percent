import json
import logging
import os
import sys
import time
from typing import Dict

import schedule  # type: ignore

from src.core import SixPercent
from src.gui import login_gui
from src.utils.constants import ASNB_COOLDOWN_PERIOD, ASNB_LOGIN_URL, CHROME_DRIVER_PATH
from src.utils.encryption import decrypt_password
from src.utils.log import log_errors

logging.basicConfig(level=logging.INFO)


def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller
    """
    try:
        base_path = sys._MEIPASS  # type: ignore

    except Exception:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)


@log_errors()
def main(user_credentials: Dict[str, str]) -> None:
    logging.info("Starting Six Percent Bot")

    bot = SixPercent(
        url=ASNB_LOGIN_URL,
        chrome_driver_path=resource_path(CHROME_DRIVER_PATH),
    )

    logging.info(f"Logging in as {user_credentials['username']}")
    investment_amount = user_credentials["investment_amount"]
    asnb_username = user_credentials["username"]
    hashed_asnb_password = user_credentials["password"]

    asnb_password = decrypt_password(hashed_asnb_password)

    # Login
    bot.launch_browser()
    bot.login(asnb_username, asnb_password)

    # Updates user.json when login is successful
    with open("user.json", "w") as u:
        json.dump(user_credentials, u)

    bot.purchase(investment_amount)
    logging.info(f"Repeating job after {ASNB_COOLDOWN_PERIOD} minutes")


if __name__ == "__main__":
    user_credentials = login_gui()

    # Loads user configuration from user.json
    try:
        if bool(user_credentials) is False:
            with open("user.json", "r") as u:
                user_credentials = json.load(u)

    except FileNotFoundError:
        logging.error("No user found. Please login as new user")
        sys.exit()

    # Run job once on start
    main(user_credentials)

    # Schedule job every ASNB_COOLDOWN_PERIOD minutes
    schedule.every(ASNB_COOLDOWN_PERIOD).minutes.do(main, user_credentials)

    while True:
        schedule.run_pending()
        time.sleep(1)
