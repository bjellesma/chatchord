import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models.models import RoomsModel, BotsModel

class Rooms(MongoengineObjectType):
    class Meta:
        model = RoomsModel
        interfaces = (Node,)

class Bots(MongoengineObjectType):
    class Meta:
        model = BotsModel
        interfaces = (Node,)

class Query(graphene.ObjectType):
    node = Node.Field()
    all_bots = MongoengineConnectionField(Bots)
    all_rooms = MongoengineConnectionField(Rooms)

schema = graphene.Schema(query=Query, types=[Rooms, Bots])