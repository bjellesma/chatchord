import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from models.models import RoomsModel, BotsModel, UsersModel

class Users(MongoengineObjectType):
    class Meta:
        model = UsersModel
        interfaces = (Node,)

class Rooms(MongoengineObjectType):
    class Meta:
        model = RoomsModel
        interfaces = (Node,)

class Bots(MongoengineObjectType):
    class Meta:
        model = BotsModel
        interfaces = (Node,)

class CreateUser(graphene.Mutation):
    user = graphene.Field(Users)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = UsersModel(
            username=username,
            password_hash=password
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class Query(graphene.ObjectType):
    node = Node.Field()
    all_bots = MongoengineConnectionField(Bots)
    all_rooms = MongoengineConnectionField(Rooms)
    all_users = MongoengineConnectionField(Users)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation, types=[Rooms, Bots, Users])