from typing import List

from bs4 import BeautifulSoup
from src.utils.constants import DESKTOP_TX_CLASS, MOBILE_TX_CLASS


def process_html(page: BeautifulSoup) -> None:
    tx_hashes = extract_tx_hashes(page)

    for h in tx_hashes:
        print(h)


def extract_tx_hashes(page: BeautifulSoup) -> List[str]:
    mobile = False
    tx_containers = page.findAll('ul', class_=DESKTOP_TX_CLASS)

    if not tx_containers:
        mobile = True
        tx_containers = page.findAll('div', class_=MOBILE_TX_CLASS)

    tx_hashes = []

    if len(tx_containers) == 0:
        tx_hashes.append("No tx hashes found")
    else:
        if mobile:
            for tx in tx_containers:
                if "/fetchai/validators/" not in tx.a.get('href'):
                    tx_hashes.append(tx.a.get('href'))
        else:
            for tx in tx_containers:
                if "/fetchai/validators/" not in tx.li.a.get('href'):
                    tx_hashes.append(tx.li.a.get('href'))

    return tx_hashes
