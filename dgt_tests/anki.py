import logging

import genanki
import os
from urllib.parse import urlparse

from .conf import settings

from .models import Question, Answer
from .media import get_crawl_image_media_path


test_model = genanki.Model(
    1596048153,
    "Test DGT",
    fields=[
        {'name': 'Question'},
        {'name': 'Answer'},
        {'name': 'Image'}, 
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Image}}{{Question}}",
            "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
        },
    ],
)


class AnkiPacker:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def run(self):
        deck = genanki.Deck(1596048154, "Tests DGT")
        pack = genanki.Package(deck)

        for question in Question.select():
            note_question = f'<p>{question.text}</p><ul>'
            for answer in question.answers:
                note_question += f'<li><strong>{answer.letter})</strong> {answer.text}</li>'
            note_question += '</ul>'

            self.logger.info("Creating note: %s", note_question)

            note_answer = f'<p><strong>{question.correct_answer}</strong></p>'
            
            # Media files should have unique filenames.
            image_media_path = get_crawl_image_media_path(question.image)
            note_image = f'<img src="{os.path.basename(image_media_path)}"/>'
            pack.media_files.append(image_media_path)
            

            note = genanki.Note(
                model=test_model,
                fields=[
                    note_question,
                    note_answer,
                    note_image,
                ],
            )
            deck.add_note(note)
            
        self.logger.info("Packing...")
        pack.write_to_file(f"{settings.DATA_PATH}/tests-dgt.apkg")
        self.logger.info("Done")




