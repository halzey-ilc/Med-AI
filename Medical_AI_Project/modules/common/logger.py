import logging
import os
from datetime import datetime


class Logger:
    """
    A custom logger for handling logs across the application.
    """

    LOG_DIR = "logs"

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    def __init__(self, name: str, log_level=logging.INFO):
        """
        Initializes a logger instance.

        :param name: The name of the logger.
        :param log_level: Logging level (default is INFO).
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Avoid duplicate handlers
        if not self.logger.hasHandlers():
            log_filename = os.path.join(self.LOG_DIR, f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log")

            # File handler
            file_handler = logging.FileHandler(log_filename, mode="a", encoding="utf-8")
            file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, message: str):
        """ Logs an informational message. """
        self.logger.info(message)

    def warning(self, message: str):
        """ Logs a warning message. """
        self.logger.warning(message)

    def error(self, message: str):
        """ Logs an error message. """
        self.logger.error(message)

    def debug(self, message: str):
        """ Logs a debug message. """
        self.logger.debug(message)


# Example Usage
if __name__ == "__main__":
    logger = Logger("TestLogger")
    logger.info("This is an informational log.")
    logger.warning("This is a warning log.")
    logger.error("This is an error log.")
    logger.debug("This is a debug log.")
