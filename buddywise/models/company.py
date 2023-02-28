from mongoengine import Document, StringField


class Company(Document):
    guid = StringField(required=True, unique=True)
    name = StringField(required=True)
