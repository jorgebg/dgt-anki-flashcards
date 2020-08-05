import argparse
import logging
import os
from importlib import import_module
from .conf import settings

from .anki import AnkiPacker

parser = argparse.ArgumentParser()
parser.add_argument("action", help='"crawl" action downloads the tests, while "anki" action generates the anki package',
                    type=str, choices=["crawl", "anki"])
parser.add_argument('--verbose', '-v', action='store_true', help='verbose output')
args = parser.parse_args()
if args.verbose:
    logging.basicConfig(level=logging.INFO)
if args.action == "crawl":
    for dotted_path in settings.CRAWLERS:
        module_path, class_name = dotted_path.rsplit('.', 1)
        crawler_class = getattr(import_module(module_path), class_name)
        crawler_class().run()
elif args.action == "anki":
    AnkiPacker().run()