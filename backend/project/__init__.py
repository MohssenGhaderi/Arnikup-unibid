__version__ = '0.2'
# import eventlet
# eventlet.monkey_patch()
import gevent
from gevent import monkey
monkey.patch_all()

from functools import wraps
from flask import Blueprint,Flask , session , Response , render_template ,request, g, jsonify, make_response, url_for
# from flask_restful import reqparse, abort, Api, Resource
import flask_restful,flask_restplus
from datetime import timedelta
from flask_debugtoolbar import DebugToolbarExtension
from flask_jwt_extended import JWTManager
# from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_socketio import SocketIO

import redis
from flask_login import current_user,LoginManager
from definitions import SESSION_EXPIRE_TIME,SMS_USERNAME,SMS_PASSWORD
from flask_session import Session
from sqlalchemy import create_engine
from flask_mail import Mail
from flask_cors import CORS
from .exceptions import ValidationException
from .lang.fa import TOKEN
import jwt as original_jwt
import rejson

# class CustomApi(flask_restful.Api):
#     def handle_error(self, e):
#         print (make_response(jsonify({"error":str(e)}),500))
#         return 'ok'

import warnings
warnings.filterwarnings("ignore")

REDIS_URL = "redis://localhost:6379/0"

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
redis_db = redis.Redis(connection_pool=pool)

rj = rejson.Client(host='localhost', port=6379,decode_responses=True)

app = Flask(__name__)
app.config.from_pyfile('config.py')

mail = Mail(app)
jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return model.Revoked.is_jti_blacklisted(jti)

# after production comment this
# Session(app)

params = {
	 'pingInterval': 20000,
     'pingTimeout': 10000,
}
#
# socketio = SocketIO(logger=True, engineio_logger=True, **params)

socketio = SocketIO(**params)
socketio.init_app(app, message_queue=REDIS_URL,async_mode='gevent',manage_session=False)

app.debug = False
toolbar = DebugToolbarExtension(app)

#login manager

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'site.login'

@app.before_request
def make_session_permanent():
    session.permanent = True
    session.modified = True
    session.permanent_lifetime = timedelta(days=SESSION_EXPIRE_TIME)

def verify_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            if not current_user.is_verified:
                return render_template('site/verify.html'), 400
            else:
                return fn(*args, **kwargs)
        else:
            return fn(*args, **kwargs)
    return wrapper

def iverify_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            if not current_user.is_verified:
                return render_template('site/iframes/verify.html'), 400
            else:
                return fn(*args, **kwargs)
        else:
            return fn(*args, **kwargs)
    return wrapper

from project.middleware import *
app.jinja_env.globals.update(has_role=has_role)

# csrf = CSRFProtect(app)

# from .route import route

@app.route('/')
def site():
    return make_response('everythins works fine')

rest_api = flask_restplus.Api(app,'/v2/api')
blueprint = Blueprint('rest_api', __name__, url_prefix='/v2/api')
rest_api = flask_restplus.Api(blueprint, doc='/doc/',
version="2.0",
title="Unibid API",
description="This is v2 unibid api documentation.",
default="API Documentation",
default_label="Unibid v2 api documentation")

CORS(blueprint)

# @blueprint.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,User-Agent')
#     response.headers.add('Access-Control-Allow-Methods', 'POST')
#     return response

# api = flask_restful.Api(app,'/api')

from .websocket import handler
from .controllers import *
from .resources.auth import auth_ns
from .resources.site import site_ns
from .resources.auction import auction_ns
from .resources.shop import shop_ns
from .resources.buy import buy_ns
from .resources.user import user_ns

@rest_api.errorhandler(ValidationException)
def handle_validation_exception(error):
    return {'message': 'Validation error', 'errors': {error.error_field_name: error.message}}, 400


@rest_api.errorhandler(original_jwt.ExpiredSignatureError)
def handle_expired_signature_error(error):
    return {'message': TOKEN['expired']}, 401

@rest_api.errorhandler(original_jwt.InvalidTokenError)
def handle_invalid_token_error(error):
    return {'message': TOKEN['malformed']}, 401

@rest_api.errorhandler(original_jwt.DecodeError)
def handle_invalid_token_error(error):
    return {'message': TOKEN['decode']}, 401

@rest_api.errorhandler(original_jwt.InvalidIssuerError)
def handle_invalid_token_error(error):
    return {'message': TOKEN['issue']}, 401

rest_api.add_namespace(auth_ns)
rest_api.add_namespace(site_ns)
rest_api.add_namespace(auction_ns)
rest_api.add_namespace(shop_ns)
rest_api.add_namespace(buy_ns)
rest_api.add_namespace(user_ns)
app.register_blueprint(blueprint)
