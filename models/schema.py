import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models.rooms import RoomsModel

class Rooms(MongoengineObjectType):
    class Meta:
        model = RoomsModel
        interfaces = (Node,)

class Query(graphene.ObjectType):
    node = Node.Field()
    all_rooms = MongoengineConnectionField(Rooms)

schema = graphene.Schema(query=Query, types=[Rooms])