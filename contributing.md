Data is designed to be received on the server via GraphQL and was originally written on a MongoDB Database hence the graphene_mongo package. The following is a way to create your own data.
1. Create Data

Using the MongoDB database that you've connected to, create a collection of the data that you want.

2. Create a model on the server

Head to chatchord/models/models.py and create a class following the below structure

```py
class ClassName(Document):

    meta = {'collection': "collection_name"}
    name = StringField()
```

where ClassName is the camel cased name of the collection follow by `Model`. For example, if your collection is chats, ClassName would be `ChatsModel`
where collection_name is the name of the collection in MongoDB

3. Import your model

Head to chatchord/models/schema.py and import the model that you've just created. You should see a line at the top of the file saying `from models.models import RoomsModel, BotsModel`. Simply insert your model from the previous step to this import llist.

4. Create a schema class

Add a schema class with the following structure:

```py
class Class(MongoengineObjectType):
    class Meta:
        model = ModelName
        interfaces = (Node,)
```

where Class matches the capitalized version of the collection that you've created in mongodb. For Example, if the collection that you made is called chats, the class would be `Chats`.
where ModelName is the name of the imported model that you've made.

5. Modify the schema object

Modify the types on the schema object to include the schema class that you've created. The schema object should be the last line in the file and look lik

```py
schema = graphene.Schema(query=Query, types=[Rooms, Bots])
```