from mongoengine import connect
import settings 

database_type = settings.DBTYPE
database_user = settings.DBUSER
database_password = settings.DBPASSWORD
database_host = settings.DBHOST
database_port = settings.DBPORT
database_name = settings.DBNAME
connect_string = f'{database_type}://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}'

# You can connect to a real mongo server instance by your own.
connect('mongo_instance', host=connect_string, alias='default', retryWrites=False)
# import pymongo
# import settings 
# from settings import ColorMessages

# # NOTE testing
# import pprint




# # Connect to database
# # We try to connect to the database
# try:
#     database_client = pymongo.MongoClient(connect_string, serverSelectionTimeoutMS=3000)
# except Exception as error:
#     print(f'{ColorMessages.FAIL}Invalid connect string: {connect_string}{ColorMessages.ENDC}')
# try:
#     # an error will be thrown if we can't get the server info
#     database_client.server_info()
#     print(f'{ColorMessages.OKGREEN}The database connection was successful{ColorMessages.ENDC}')
# except Exception as error:
#     print(f'{ColorMessages.FAIL}An error occured making a connection to the host\nError: {error}{ColorMessages.ENDC}')

# try:
#     db = database_client[database_name]
# except Exception as error:
#     print(f'{ColorMessages.FAIL}The database {database_name} was unable to be reached\nError: {error}{ColorMessages.ENDC}')