from project.db_config import Config
import os
import definitions
from datetime import datetime,timedelta

# Create dummy secrey key so we can use sessions
# SECRET_KEY = "1qsj59$80__+j3o0-1cn.f=20-=@$&mp=-d1hkpwqhf2-==123ehdwoh^2n-^$@8-jf[=2ufiofh]"
# JWT_SECRET_KEY = "=921nlkwendq-019-4=1%@$-igj2f-=@FF2jpw00-=02=fjng809=292fj-209r=548@$Gdjp="
# SECRET_KEY = os.urandom(124)
JWT_SECRET_KEY = os.urandom(124)
DEBUG_TB_INTERCEPT_REDIRECTS = False
# SESSION_TYPE = 'filesystem'

SECRET_KEY = os.urandom(64)
SESSION_TYPE = 'null'
SESSION_COOKIE_NAME = 'unibid session'
SESSION_PERMANENT = True
PERMANENT_SESSION_LIFETIME = timedelta(days=31) #(2678400 seconds)

# Create in-memory database

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = Config.engine + '://' + Config.username + ':' + Config.password + '@' + Config.host_name + ':' + Config.port + '/' + Config.db_name
SQLALCHEMY_ECHO = False
# SQLALCHEMY_MAX_CLIENT_CONN = 500
#
SQLALCHEMY_POOL_SIZE = 500
# SQLALCHEMY_POOL_RECYCLE = 3600
# SQLALCHEMY_MAX_OVERFLOW = 1000
# SQLALCHEMY_POOL_TIMEOUT = 30

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
JWT_TOKEN_LOCATION = 'cookies'
JWT_COOKIE_CSRF_PROTECT = True
JWT_ACCESS_TOKEN_EXPIRES = True
# JWT_REFRESH_TOKEN_EXPIRES = False
JWT_COOKIE_SECURE = False
# JWT_SESSION_COOKIE = True
JWT_EXPIRATION_DELTA = timedelta(days=7)
JWT_VERIFY_EXPIRATION = False

JWT_ACCESS_COOKIE_PATH = '/api/'
JWT_REFRESH_COOKIE_PATH = '/api/'

REMEMBER_COOKIE_DURATION = timedelta(days=31)
REMEMBER_COOKIE_SECURE = True


# Disable CSRF protection for this example. In almost every case,
# this is a bad idea. See examples/csrf_protection_with_cookies.py
# for how safely store JWTs in cookies
# JWT_COOKIE_CSRF_PROTECT = False

# CACHE_TYPE = 'simple'

# UPLOAD ATACHMENTS
UPLOAD_FOLDER = definitions.UPLOAD_FOLDER

# mail config

MAIL_SERVER = "mail.unibid.ir"
MAIL_PORT = 25
MAIL_USE_TLS = True
# MAIL_USE_SSL = True
# MAIL_DEBUG : default app.debug
MAIL_USERNAME  = "hostmaster"
MAIL_PASSWORD = "123mail321"
# MAIL_DEFAULT_SENDER : default None
# MAIL_MAX_EMAILS : default None
# MAIL_SUPPRESS_SEND : default app.testing
# MAIL_ASCII_ATTACHMENTS : default False

PROPAGATE_EXCEPTIONS = False
DEBUG = False

VERIFY_USER_TOKEN_TIME =  1 * 1 * 2 * 60 # 2 minute
ONLINE_USER_ACCESS_TIME =  1 * 2 * 60 * 60 # 2 hours
# ONLINE_USER_ACCESS_TIME =  1 * 1 * 1 * 60 # 1 minute
ONLINE_USER_REFRESH_TIME = 15 * 24 * 60 * 60  # 15 days
