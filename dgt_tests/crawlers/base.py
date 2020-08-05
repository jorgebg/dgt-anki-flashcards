import logging
import os

import requests
from bs4 import BeautifulSoup

from dgt_tests.media import download_image, get_crawl_image_media_path
from dgt_tests.models import Question, Answer

def field(fun):
    fun.is_field = True
    return fun

def get_fields(obj):
    fields = []
    for key in dir(obj):
        value = getattr(obj, key)
        if getattr(value, 'is_field', False):
            fields.append(key)
    return fields


class BaseItem:
    def __init__(self, parent_node):
        self.node = parent_node

    def to_dict(self):
        return {key: getattr(self, key)() for key in get_fields(self)}

    @classmethod
    def find_items(cls, html):
        root = cls(html)
        return [cls(node) for node in root.find_nodes()]

    def find_nodes(self):
        raise NotImplementedError("BaseItem.find_nodes")


class BaseCrawler:
    
    question_exporter = None
    answer_exporter = None

    def __init__(self):
        self.name = self.__class__.__name__.strip('Crawler')
        self.logger = logging.getLogger(__name__)

    def get_test_urls(self):
        raise NotImplementedError('BaseCrawler.get_test_urls')

    def is_test_crawled(self, test_url):
        return Question.select().where(Question.test_url==test_url).exists()

    def run(self):
        self.logger.info("Starting %s crawler", self.name)
        for test_url in self.get_test_urls():
            if self.is_test_crawled(test_url):
                continue
            resp = requests.get(test_url)
            if resp.status_code == 200:
                self.logger.info("Processing test: %s", test_url)
            else:
                self.logger.info("Test not found: %s", test_url)
                continue
            html = BeautifulSoup(resp.content, 'html.parser')
            for question_item in self.question_exporter.find_items(html):
                question = self.get_or_create(Question, crawler=self.name, test_url=test_url, **question_item.to_dict())
                for answer_item in self.answer_exporter.find_items(question_item.node):
                    answer = self.get_or_create(Answer, question=question, **answer_item.to_dict())
                download_image(question.image)

    def get_or_create(self, model, **attributes):
        instance, created = model.get_or_create(**attributes)
        if created:
            self.logger.info("%s CREATED: %s", model._meta.name, instance)
        else:
            self.logger.info("%s SKIPPED: %s", model._meta.name, instance)
        return instance


