# NOTE importing the mongobase alone is enough to initiate the connection
import models.mongobase
from mongoengine import Document
from mongoengine.fields import (
    StringField, ListField
)
import pprint

class RoomsModel(Document):

    meta = {'collection': "rooms"}
    name = StringField()

class BotsModel(Document):

    meta = {'collection': "bots"}
    name = StringField()
    phrases = ListField(StringField())