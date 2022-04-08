import pytest

from .config import test_config

from src.models import TxDetailScraper
from src.utils.constants import URL


@pytest.fixture
def get_subject(test_config):
    detail_extractor = TxDetailScraper(
        config=test_config, tx_hash_links=[
            f"{URL}/txs/62E0D7496B98E51C868BF028DF75163D0DCF1ACEC3A0B1547A1A9FE38E9D7BF7",
            f"{URL}/txs/6A22CFFE0BF8D7DF255F5385DB16988FF136B55B63BD24FADFDC0CD3295084F2",
            f"{URL}/txs/83627715AF05765712CC7AB5EC6CB431DC64EA7A847716A341862A8EAB2EDD1B",
            f"{URL}/txs/1AB09BDFB0CBF16B3CDCD1A6BBE5429EC038F4C61B0D8F463877E7F7D2388F0D",
            f"{URL}/txs/4AFB198EFF07B1C9F05C84596FBA472CEBC5FE3536C8330261EAD3B28D5C5088",
            f"{URL}/txs/6A72E406D556D95D47CBFF9DAB86C74EB93664936DEBA03FC2428D8CAC1BD860",
        ]
    )

    return detail_extractor


def test_initiate(get_subject):
    get_subject.config.driver.minimize_window()

    transactions = get_subject.initiate()

    for t in transactions:
        print(t.__dict__)
