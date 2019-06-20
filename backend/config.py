from project.db_config import Config
import os
import definitions
from datetime import datetime,timedelta

SECRET_KEY = os.urandom(64)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = Config.engine + '://' + Config.username + ':' + Config.password + '@' + Config.host_name + ':' + Config.port + '/' + Config.db_name
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_SIZE = 500
