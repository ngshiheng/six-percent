import functools
import logging
from logging import Logger


def _generate_log(path: str) -> Logger:
    """
    Creates a logger object
    """

    # Creates a logger and set the level.
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    # Creates file handler, logs format and adds the format to file handler
    file_handler = logging.FileHandler(path)

    log_format = '%(levelname)s %(asctime)s %(message)s'
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
# end def


def log_errors(path: str = 'errors.log'):
    """
    Creates a parent function to take arguments
    """

    def error_log(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            try:
                # Executes the called function
                # If it throws an error `Exception` will be called
                # Otherwise it will be execute successfully
                return func(*args, **kwargs)

            except Exception as e:

                logger = _generate_log(path)
                logger.exception(f"An error has occurred at /{func.__name__}\n")
                return e
            # end try
        # end def

        return wrapper
    # end def

    return error_log
# end def
