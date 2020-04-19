# NOTE importing the mongobase alone is enough to initiate the connection
import models.mongobase
from mongoengine import Document
from mongoengine.fields import (
    DateTimeField, ReferenceField, StringField,
)
import pprint

class RoomsModel(Document):

    meta = {'collection': "rooms"}
    name = StringField()

class BotsModel(Document):

    meta = {'collection': "bots"}
    name = StringField()