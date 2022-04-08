import re
from datetime import datetime

from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

from src.models import Configuration
from src.models.tx import Transaction
from src.utils.constants import (
    TX_MSG_INFO_SECTION_CLASS,
    TX_MSG_INFO_SECTION_ROW_CLASS,
    TX_MSG_INFO_SECTION_ROW_LABEL_CLASS,
    TX_MSG_INFO_SECTION_ROW_VALUE_CLASS,
    TX_MSG_MESSAGES_WRAPPER_CLASS,
    TX_MSG_MESSAGE_INFO_CLASS,
    TX_MSG_MESSAGE_INFO_LABEL_CLASS,
    TX_MSG_MESSAGE_INFO_VALUE_CLASS,
)


class TxDetailScraper:
    def __init__(self, config: Configuration, tx_hash_links: List[str]):
        self.config = config
        self.tx_hash_links = tx_hash_links

    def initiate(self) -> List[Transaction]:
        transactions = []

        for link in self.tx_hash_links:
            self.load_page(link)

            transaction = Transaction()

            self.extract_details(transaction)

            if transaction.valid is True:
                transactions.append(transaction)

        return transactions

    def load_page(self, url: str):
        self.config.driver.get(url)

        required_elements = EC.presence_of_element_located(
            (By.CLASS_NAME, TX_MSG_INFO_SECTION_CLASS))

        WebDriverWait(self.config.driver, 10).until(required_elements)

        required_elements = EC.presence_of_element_located(
            (By.CLASS_NAME, TX_MSG_MESSAGES_WRAPPER_CLASS))

        WebDriverWait(self.config.driver, 10).until(required_elements)

    def extract_details(self, transaction: Transaction):
        required_elements = EC.presence_of_element_located(
            (By.CLASS_NAME, TX_MSG_INFO_SECTION_CLASS))

        page = WebDriverWait(self.config.driver, 10).until(required_elements)

        self.extract_info(info_element=page, transaction=transaction)

        required_elements = EC.presence_of_element_located(
            (By.CLASS_NAME, TX_MSG_MESSAGES_WRAPPER_CLASS))

        page = WebDriverWait(self.config.driver, 10).until(required_elements)

        self.extract_messages(messages_element=page, transaction=transaction)

    @staticmethod
    def extract_info(info_element: WebElement, transaction: Transaction):
        info_rows = info_element.find_elements(By.CLASS_NAME, TX_MSG_INFO_SECTION_ROW_CLASS)

        for row in info_rows:
            row_label = row.find_element(By.CLASS_NAME, TX_MSG_INFO_SECTION_ROW_LABEL_CLASS)
            row_value = row.find_element(By.CLASS_NAME, TX_MSG_INFO_SECTION_ROW_VALUE_CLASS)

            if row_label.text == "TxHash":
                transaction.tx_hash = row_value.text

            if row_label.text == "Status" and row_value.text == "Success":
                transaction.valid = True

            if row_label.text == "Time":
                value = re.sub(r'[0-9A-Za-z\s]+ ago\b', '', row_value.text)
                value = re.sub('[()]', '', value).strip()

                time = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')

                transaction.time = time

            if row_label.text == "Fee":
                currency = re.sub('[\d]+', '', row_value.text).strip('.')
                transaction.fee_currency = currency

                fee = re.sub(currency, '', row_value.text)
                transaction.fee = fee

    @staticmethod
    def extract_messages(messages_element: WebElement, transaction: Transaction):
        # TX_MSG_MESSAGE_INFO_CLASS,
        # TX_MSG_MESSAGE_INFO_LABEL_CLASS,
        # TX_MSG_MESSAGE_INFO_VALUE_CLASS
        pass
