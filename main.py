import json
import logging
import logging.config
import os
import sys
import time
from typing import Dict

from src.bot import SixPercent
from src.encryption import decrypt_password
from src.gui import login_gui
from src.settings import ASNB_LOGIN_URL, BOT_COOLDOWN_INTERVAL, CHROME_DRIVER_PATH, LOGGING_CONFIG, USER_CONFIG_PATH

logger = logging.getLogger("sixpercent")


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource

    works for PyInstaller and local development"""
    try:
        base_path = sys._MEIPASS  # type: ignore

    except Exception:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)


def display_gui() -> Dict[str, str]:
    try:
        user_credentials = login_gui()
        if bool(user_credentials) is False:
            with open(USER_CONFIG_PATH, "r") as u:
                user_credentials = json.load(u)

        return user_credentials

    except FileNotFoundError:
        logger.warning("No existing user found. Please login as new user")
        sys.exit()


def run_six_percent_bot(user_credentials: Dict[str, str]) -> None:
    logger.info("Starting Six Percent Bot")
    bot = SixPercent(
        url=ASNB_LOGIN_URL,
        chrome_driver_path=resource_path(CHROME_DRIVER_PATH),
    )

    asnb_username = user_credentials["username"]
    encrpyted_asnb_password = user_credentials["password"]
    asnb_password = decrypt_password(encrpyted_asnb_password)

    payment_method = user_credentials["payment_method"]
    investment_amount = user_credentials["investment_amount"]

    bot.launch_browser()
    bot.login(asnb_username, asnb_password)

    with open(USER_CONFIG_PATH, "w") as u:  # NOTE: Always updates `user.json` upon successful login
        json.dump(user_credentials, u)

    bot.purchase(investment_amount, payment_method)
    logger.info("Completed job")


def entrypoint() -> None:
    try:
        user_credentials = display_gui()
        while True:
            run_six_percent_bot(user_credentials)
            logger.info("Rerunning Six Percent Bot after 5 minutes")
            time.sleep(BOT_COOLDOWN_INTERVAL)

    except KeyboardInterrupt:
        logger.warning("Exiting. Program interrupted manually")
        sys.exit()

    except Exception as e:
        logger.exception(e)
        raise


def main() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
    entrypoint()


if __name__ == "__main__":
    main()
