import logging

from requests_html import HTMLSession
from bs4 import BeautifulSoup

from src.utils.process_data import process_html

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_pages(url: str):
    logger.info(f"Starting session for account {url}")
    session = HTMLSession()

    response = session.get(url)
    response.html.render(sleep=1, keep_page=True, scrolldown=3)

    html = response.html.html

    soup = BeautifulSoup(html, 'html.parser')

    process_html(soup)
