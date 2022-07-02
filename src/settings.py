import os

# General
# -------
USER_CONFIG_PATH = os.path.join('user.json')
CHROME_DRIVER_PATH = os.path.join('bin', 'driver', 'chromedriver.exe')


ASNB_LOGIN_URL = "https://www.myasnb.com.my/login"
TOTAL_FUND_COUNT = 3
MAX_PURCHASE_RETRY_ATTEMPTS = 10


# Time
# ----
TIMEOUT_LIMIT = 25  # seconds
BOT_COOLDOWN_INTERVAL = 300  # seconds
PAYMENT_TIMEOUT_LIMIT = 300  # seconds


# Logging
# -------
ERROR_LOG_FILENAME = "sixpercent-errors.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            'format': "%(asctime)s %(levelname)s %(message)s",
            "datefmt": "%d-%b-%Y %H:%M:%S",
        },
        "colored": {
            '()': 'colorlog.ColoredFormatter',
            'format': "%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
            "datefmt": "%d-%b-%Y %H:%M:%S",
        },
        "simple": {
            "format": "%(message)s",
        },
    },
    "handlers": {
        "logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "filename": ERROR_LOG_FILENAME,
            "formatter": "default",
            "backupCount": 2,
        },
        "verbose_output": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "sixpercent": {
            "level": "INFO",
            "handlers": [
                "verbose_output",
            ],
        },
    },
    "root": {"level": "INFO", "handlers": ["logfile"]},
}
