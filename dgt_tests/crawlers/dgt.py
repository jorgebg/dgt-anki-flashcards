import re

import requests
from bs4 import BeautifulSoup

from .base import BaseCrawler, BaseItem, field


INITIAL_TEST_NUMBER = 224

class QuestionItem(BaseItem):

    def find_nodes(self):
        return self.node.find_all("article", class_="test")

    @field
    def text(self):
        text = self.node.find('h4', class_='tit_not').text
        return re.search(r"\d+\. (.*)", text).group(1)
    
    @field
    def correct_answer(self):
        return self.node.find('div', class_='content_respuesta').find('span', class_='opcion').text.upper()
    
    @field
    def image(self):
        return "http://revista.dgt.es" + self.node.find("img")["src"]
    


class AnswerItem(BaseItem):

    def find_nodes(self):
        return self.node.find('ul').find_all('li')

    @field
    def letter(self):
        return self.node.find('span', class_='opcion').text.strip('.').upper()

    @field
    def text(self):
        return list(self.node.children)[1].strip()



class DGTCrawler(BaseCrawler):

    question_exporter = QuestionItem
    answer_exporter = AnswerItem

    def get_test_urls(self):
        resp = requests.get("http://revista.dgt.es/es/test/")
        html = BeautifulSoup(resp.content, 'html.parser')
        test_index = html.find('section', id="enlaces_relacionados")
        previous_test_number = int(re.search(r"\d+", test_index.find('a')['href']).group())
        last_test_number = previous_test_number + 1
        test_numbers = range(INITIAL_TEST_NUMBER, last_test_number + 1)
        url_template = "http://revista.dgt.es/es/test/Test-num-{n}.shtml"
        return (url_template.format(n=n) for n in test_numbers)
