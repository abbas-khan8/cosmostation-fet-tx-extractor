import logging
import pytest

from freezegun import freeze_time
from datetime import datetime
from src.models import Configuration, TxDetailScraper
from src.utils.constants import FET_ADDRESS, URL

logging.basicConfig(level=logging.INFO)

test_logger = logger = logging.getLogger("TX-SCRAPER-LOG")


@freeze_time("2022-08-04 12:00:00")
@pytest.fixture
def test_config():
    config = Configuration(
        address=FET_ADDRESS, start_date=datetime.now(), end_date=datetime.now(), logger=test_logger
    )

    return config



