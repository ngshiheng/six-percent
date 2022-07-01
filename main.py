import json
import logging
import os
import sys
import time
from typing import Dict

from src.core import SixPercent
from src.gui import login_gui
from src.utils.constants import ASNB_COOLDOWN_SECONDS, ASNB_LOGIN_URL, CHROME_DRIVER_PATH, CONFIG_FILENAME
from src.utils.encryption import decrypt_password
from src.utils.log import log_errors

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def resource_path(relative_path: str) -> str:
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS  # type: ignore

    except Exception:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)


@log_errors()
def main(user_credentials: Dict[str, str]) -> None:
    bot = SixPercent(
        url=ASNB_LOGIN_URL,
        chrome_driver_path=resource_path(CHROME_DRIVER_PATH),
    )

    investment_amount = user_credentials["investment_amount"]
    asnb_username = user_credentials["username"]
    encrpyted_asnb_password = user_credentials["password"]
    asnb_password = decrypt_password(encrpyted_asnb_password)

    bot.launch_browser()
    bot.login(asnb_username, asnb_password)

    with open(CONFIG_FILENAME, "w") as u:  # NOTE: Always updates `user.json` upon successful login
        json.dump(user_credentials, u)

    bot.purchase(investment_amount)


if __name__ == "__main__":
    """Entry point of Six Percent Bot"""
    try:
        user_credentials = login_gui()
        if bool(user_credentials) is False:
            with open(CONFIG_FILENAME, "r") as u:
                user_credentials = json.load(u)

        while True:
            logger.info("Starting Six Percent Bot")
            main(user_credentials)
            logger.info("Repeating job after 5 minutes")
            time.sleep(ASNB_COOLDOWN_SECONDS)

    except FileNotFoundError:
        logger.error("No user found. Please login as new user")
        sys.exit()

    except KeyboardInterrupt:
        logger.info("Program interrupted manually. Goodbye")
        sys.exit()

    except Exception as e:
        logger.error(e)
        raise
