import logging

from src.models.scraper import TransactionScraper
from src.utils.constants import FET_ADDRESS
from src.utils.exceptions import MissingDriverException

logging.basicConfig(level=logging.INFO)


def run():
    logger = logging.getLogger("TX-SCRAPER-LOG")

    try:
        scraper = TransactionScraper(FET_ADDRESS, logger)
        scraper.initiate()

    except MissingDriverException as e:
        logger.info(e)
