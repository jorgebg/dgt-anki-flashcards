import json

from peewee import SqliteDatabase, CharField, Model, TextField, ForeignKeyField, Field

from .conf import settings

db = SqliteDatabase(f"{settings.DATA_PATH}/db.sqlite3")

class JSONField(Field):
    field_type = 'json'

    def db_value(self, value):
        return json.dumps(value) if value else None

    def python_value(self, value):
        return json.loads(value) if value else None

class BaseModel(Model):
    def __str__(self):
        return self.text

    class Meta:
        database = db

class Question(BaseModel):
    crawler = CharField
    test_url = CharField()
    text = TextField()
    correct_answer = CharField(max_length=1)
    image = CharField(null=True)
    extra = JSONField(null=True)



class Answer(BaseModel):
    question = ForeignKeyField(Question, backref="answers")
    letter = CharField(max_length=1)
    text = CharField()



db.connect()
db.create_tables([Question, Answer])
