import os

DATA_PATH = '.state' if os.getenv('GITHUB_ACTIONS', False) else 'data'

CRAWLERS = [
    'dgt_tests.crawlers.dgt.DGTCrawler',
]
