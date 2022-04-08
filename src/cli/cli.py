import logging
from datetime import datetime

from src.models import Configuration, TxHashScraper
from src.utils.constants import FET_ADDRESS
from src.utils.exceptions import MissingDriverException

logging.basicConfig(level=logging.INFO)


def run():
    logger = logging.getLogger("TX-SCRAPER-LOG")

    config = Configuration(
        address=FET_ADDRESS, start_date=datetime.now(), end_date=datetime.now(), logger=logger
    )

    try:
        scraper = TxHashScraper(config=config)
        scraper.initiate()

    except MissingDriverException as e:
        logger.info(e)
