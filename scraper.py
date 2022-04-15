import logging

import requests
from bs4 import BeautifulSoup


logger = logging.getLogger('scraper')


def sample():
    URL = "https://tarifaluzhora.es"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.select(".inner_block.gauge_low")

    print(results)
    logger.info('{}'.format(results))
    return results
