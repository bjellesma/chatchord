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

    # rooms_collection = db['rooms']

    # @classmethod
    # def get_rooms(cls):
    #     return_list = []
    #     rooms = cls.rooms_collection.find()
    #     for room in rooms:
    #         return_list.append({
    #             "name": room["name"]
    #         })
    #     return {"rooms": return_list}