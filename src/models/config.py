import os

from selenium import webdriver
from datetime import datetime
from logging import Logger

from src.utils.exceptions import MissingDriverException
from src.utils.constants import (
    MAX_TRANSACTIONS_LIMIT,
    CHROME_DRIVER_86_PATH,
    CHROME_DRIVER_64_PATH,
    URL,
)


class Configuration:
    def __init__(self, address: str, start_date: datetime, end_date: datetime, logger: Logger):
        self.address = address
        self.start_date = start_date
        self.end_date = end_date
        self.tx_limit = MAX_TRANSACTIONS_LIMIT
        self.logger = logger

        if os.path.exists(CHROME_DRIVER_64_PATH):
            self.driver = webdriver.Chrome(CHROME_DRIVER_64_PATH)
        elif os.path.exists(CHROME_DRIVER_86_PATH):
            self.driver = webdriver.Chrome(CHROME_DRIVER_86_PATH)
        else:
            raise MissingDriverException("Could not locate file `chromedriver.exe`")
