import pathlib
import logging
import os
from urllib.parse import urlparse

import requests

from .conf import settings

logger = logging.getLogger(__name__)

def get_crawl_image_media_path(url):
    img_url = urlparse(url)
    return pathlib.Path(f'{settings.DATA_PATH}/media/crawl/{img_url.netloc}/{img_url.path}')

def get_anki_image_media_path(url):
    sha = sha256(os.path.dirname(url))
    img_filename = os.path.basename(url.path)
    img_anki_path = pathlib.Path(f'{settings.DATA_PATH}/media/anki/{sha}_{img_filename}')
    os.makedirs(os.path.dirname(img_anki_path), exist_ok=True)
    if os.path.exists(img_anki_path):
        logger.info("image SKIPPED: %s", url)
    else:
        cp(get_crawl_image_media_path(url), path)
        logger.info("image COPIED: %s", url)
    return path

def download_image(url):
    img_req = requests.get(url)
    img_media_path = get_crawl_image_media_path(url)
    os.makedirs(os.path.dirname(img_media_path), exist_ok=True)
    if os.path.exists(img_media_path):
        logger.info("image SKIPPED: %s", url)
    else:
        with open(img_media_path, "wb") as f:
            f.write(img_req.content)
        logger.info("image DOWNLOADED: %s", url)