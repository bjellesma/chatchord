# NOTE importing the mongobase alone is enough to initiate the connection
import models.mongobase
from mongoengine import Document
from mongoengine.fields import (
    StringField, ListField, BooleanField
)
from mongoengine.errors import DoesNotExist #Error Handling
from flask_login import UserMixin # user logins
from werkzeug.security import generate_password_hash, check_password_hash #password hashing
from app import login
import pprint

class UsersModel(UserMixin, Document):
    # Note: everything is camelcased in graphql so first_name becomes firstName no matter what it is in the database
    meta = {'collection': 'users'}
    username = StringField(required=True)
    password_hash = StringField(required=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def find_user_by_username(self, username):
        try:
            return UsersModel.objects.get(username=username)
        except DoesNotExist as err:
            print('No user exists with that name')
            return None

    def register(self, username, password, confirmPassword):
        # Execute the graphql mutation to register the user
        # mutation {
        #     createUser(username: "some_dude", password: "123"){
        #         user{
        #         id
        #         username
        #         }
        #     }
        # }

@login.user_loader
def load_user(id):
    return UsersModel.objects.get(id=id)

class RoomsModel(Document):

    meta = {'collection': "rooms"}
    name = StringField()
    requiresAuth = BooleanField()

class BotsModel(Document):

    meta = {'collection': "bots"}
    name = StringField()
    phrases = ListField(StringField())