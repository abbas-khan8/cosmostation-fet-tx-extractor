import os.path

from logging import Logger

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from src.utils.exceptions import MissingDriverException, RetrievalException
from src.utils.constants import (
    URL,
    TX_TABLE_CLASS,
    CHROME_DRIVER_86_PATH,
    CHROME_DRIVER_64_PATH,
    DESKTOP_TX_CLASS,
    TX_HASH_PREFIX,
    TX_PAGINATION_CONTAINER_CLASS,
    TX_CURRENT_PAGE_CLASS,
    TX_TRANSACTIONS_CLASS,
    TX_PAGE_BUTTONS_CONTAINER_CLASS,
    TX_LAST_BUTTON_CLASS,
    INACTIVE_BUTTON_CLASS,
)


class TransactionScraper:
    def __init__(self, fet_address: str, logger: Logger):
        self.fet_address = fet_address
        self.url = f"{URL}/account/{fet_address}"
        self.logger = logger

        if os.path.exists(CHROME_DRIVER_64_PATH):
            self.driver = webdriver.Chrome(CHROME_DRIVER_64_PATH)
        elif os.path.exists(CHROME_DRIVER_86_PATH):
            self.driver = webdriver.Chrome(CHROME_DRIVER_86_PATH)
        else:
            raise MissingDriverException("Could not locate file `chromedriver.exe`")

        self.tx_pages = 0
        self.pages = 0
        self.tx_hash_links = []

    def initiate(self):
        try:
            self.logger.info(f"Session started for account at: {self.url}")

            # self.driver.minimize_window()

            self.load_page()
            self.paginate_and_read_transactions()
            self.process_transactions()
            self.close_scraper()

        except (TimeoutException, RetrievalException) as e:
            self.logger.info(e)
            self.close_scraper()

    def load_page(self):
        self.driver.get(self.url)

        tx_container_present = EC.presence_of_element_located(
            (By.CLASS_NAME, TX_TABLE_CLASS))

        WebDriverWait(self.driver, 10).until(tx_container_present)

    def paginate_and_read_transactions(self):
        while True:
            pagination_container = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, TX_PAGINATION_CONTAINER_CLASS)))

            page_number_buttons = pagination_container.find_element(
                By.CLASS_NAME,
                TX_PAGE_BUTTONS_CONTAINER_CLASS
            )
            page_buttons = page_number_buttons.find_elements(By.TAG_NAME, value="button")

            current_page = pagination_container.find_element(By.CLASS_NAME, TX_CURRENT_PAGE_CLASS)

            if current_page:
                self.pages = current_page.text
            else:
                raise RetrievalException(f"Failed to retrieve page number from paginator element")

            self.extract_transactions()

            for button in page_buttons:
                element = button.find_element(By.TAG_NAME, "p")

                try:
                    page = int(element.text)

                    if page and page == int(self.pages) + 1:
                        element.click()
                        self.extract_transactions()
                        self.pages = page

                except ValueError:
                    raise RetrievalException(f"Failed to parse page number")

            pagination_container = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, TX_PAGINATION_CONTAINER_CLASS)))

            last_page_button = pagination_container.find_element(By.CLASS_NAME, TX_LAST_BUTTON_CLASS)
            button_classes = last_page_button.get_attribute("class")

            if INACTIVE_BUTTON_CLASS in button_classes:
                self.logger.info(
                    f"Successfully collected {len(self.tx_hash_links)} transactions across {self.pages} pages"
                )
                break

    def extract_transactions(self):
        try:
            tx_table = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, TX_TRANSACTIONS_CLASS)))

            transactions = tx_table.find_elements(By.CLASS_NAME, DESKTOP_TX_CLASS)

            if len(transactions) == 0:
                raise RetrievalException("No transactions found")

            for tx in transactions:
                links = set([
                    tx.get_attribute('href') for tx in tx.find_elements(by=By.TAG_NAME, value="a")
                    if tx.get_attribute('href').startswith(TX_HASH_PREFIX)
                ])

                for li in links:
                    self.tx_hash_links.append(li)

            if len(self.tx_hash_links) == 0:
                raise RetrievalException(f"No transactions were extracted")

        except Exception as e:
            raise RetrievalException(f"Failed to extract transactions: {e}")

    def process_transactions(self):
        # TODO
        pass

    def close_scraper(self):
        self.logger.info(f"Session ended for account: {self.fet_address}")
        self.driver.quit()
