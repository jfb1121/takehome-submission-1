from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmailField,
    IntField,
    ListField,
    MapField,
    StringField,
)


class Employee(Document):
    guid = StringField(required=True, unique=True)
    has_died = BooleanField(required=True)
    company_id = StringField(required=True)
    age = IntField()
    balance = StringField()
    eye_color = StringField()
    name = StringField()
    gender = StringField()
    email = EmailField()
    phone = StringField()
    address = StringField()
    about = StringField()
    registered = DateTimeField()
    tags = ListField()
    friends = ListField()
    greeting = StringField()
    favourite_food = ListField()

    meta = {"indexes": ["guid"]}
