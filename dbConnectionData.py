import os
from configparser import ConfigParser

CURRENT_PATH = os.path.dirname(__file__)
CONF_FILE_PATH = os.path.normpath(os.path.join(CURRENT_PATH, 'conf.ini'))


parser = ConfigParser()
parser.read(CONF_FILE_PATH)
DB_NAME = parser.get("DatabaseData", 'DBName')
DB_USER = parser.get("DatabaseData", 'DBRootUser')
DB_PASS = parser.get("DatabaseData", 'DBPass')