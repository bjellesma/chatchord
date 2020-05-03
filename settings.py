
import os

DBTYPE = os.environ["DB_TYPE"]
DBUSER = os.environ["DB_USER"]
DBPASSWORD = os.environ["DB_PASSWORD"]
DBHOST = os.environ["DB_HOST"]
DBPORT = os.environ["DB_PORT"]
DBNAME = os.environ["DB_NAME"]
JWT_SECRET = os.environ["JWT_SECRET"]

class ColorMessages:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'