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
