from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from src.models import Configuration


class MessageExtractor:
    def __init__(self, config: Configuration, tx_hash_links: List[str]):
        self.config = config
        self.tx_hash_links = tx_hash_links

    def initiate(self):
        self.config.logger.info("Messages extracted")
        # for tx in self.tx_hash_links:
        #     self.logger.info(tx)
