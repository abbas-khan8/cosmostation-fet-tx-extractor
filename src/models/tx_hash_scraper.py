from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from src.models import Configuration, TxDetailScraper
from src.utils.exceptions import RetrievalException
from src.utils.constants import (
    TX_CONTAINER_CLASS,
    TX_ROW_CLASS,
    TX_HASH_PREFIX,
    TX_PAGINATION_CONTAINER_CLASS,
    TX_CURRENT_PAGE_CLASS,
    TX_TABLE_CLASS,
    TX_PAGE_BUTTONS_CONTAINER_CLASS,
    TX_LAST_BUTTON_CLASS,
    TX_INACTIVE_BUTTON_CLASS, URL,
)


class TxHashScraper:
    def __init__(self, config: Configuration):
        self.config = config
        self.tx_pages = 0
        self.pages = 0
        self.tx_hash_links = []

    def initiate(self):
        try:
            self.config.logger.info(f"Session started for: {self.config.address}")

            self.config.driver.minimize_window()

            self.load_page()
            self.paginate_and_read_transactions()
            self.process_transactions()
            self.close_scraper()

        except (TimeoutException, RetrievalException) as e:
            self.config.logger.info(e)
            input()
            #self.close_scraper()

    def load_page(self):
        url = f"{URL}/account/{self.config.address}"

        self.config.driver.get(url)

        self.config.logger.info(f"Loading page for account at: {url}")

        tx_container_present = EC.presence_of_element_located(
            (By.CLASS_NAME, TX_CONTAINER_CLASS))

        WebDriverWait(self.config.driver, 10).until(tx_container_present)

    def paginate_and_read_transactions(self):
        while True:
            pagination_container = WebDriverWait(self.config.driver, 10).until(EC.presence_of_element_located(
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

            pagination_container = WebDriverWait(self.config.driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, TX_PAGINATION_CONTAINER_CLASS)))

            last_page_button = pagination_container.find_element(By.CLASS_NAME, TX_LAST_BUTTON_CLASS)
            button_classes = last_page_button.get_attribute("class")

            if len(self.tx_hash_links) >= self.config.tx_limit or TX_INACTIVE_BUTTON_CLASS in button_classes:
                self.config.logger.info(
                    f"Successfully collected {len(self.tx_hash_links)} transactions across {self.pages} pages"
                )
                break

    def extract_transactions(self):
        try:
            tx_table = WebDriverWait(self.config.driver, 10).until(EC.presence_of_element_located(
                (By.CLASS_NAME, TX_TABLE_CLASS)))

            transactions = tx_table.find_elements(By.CLASS_NAME, TX_ROW_CLASS)

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
        scraper = TxDetailScraper(config=self.config, tx_hash_links=self.tx_hash_links)

        transactions = scraper.initiate()

    def close_scraper(self):
        self.config.logger.info(f"Session ended for account: {self.config.address}")
        self.config.driver.quit()
