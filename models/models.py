# NOTE importing the mongobase alone is enough to initiate the connection
import models.mongobase
from mongoengine import Document
from mongoengine.fields import (
    StringField, ListField, BooleanField
)
import pprint

class RoomsModel(Document):

    meta = {'collection': "rooms"}
    name = StringField()
    requiresAuth = BooleanField()

class BotsModel(Document):

    meta = {'collection': "bots"}
    name = StringField()
    phrases = ListField(StringField())