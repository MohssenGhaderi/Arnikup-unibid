from json import dumps, loads, JSONEncoder, JSONDecoder
import pickle
from project import rj
from .lang.fa import TOKEN
from rejson import Path
import jwt
from flask import request, current_app
from .model.user import User
from . import rest_api


class PythonObjectEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (list, dict, str, unicode, int, float, bool, type(None))):
            return JSONEncoder.default(self, obj)
        return {'_python_object': pickle.dumps(obj)}

def as_python_object(dct):
    if '_python_object' in dct:
        return pickle.loads(str(dct['_python_object']))
    return dct

class Payload(object):
    def __init__(self, j):
        self.__dict__ = loads(j)




# required_token decorator
def token_required(f):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            rest_api.abort(401, TOKEN['required'])
        auth_header = request.headers.get('Authorization').strip()
        current_user = None
        status = 401
        message = TOKEN['unknown']
        if auth_header:
            try:
                access_token = auth_header.split(' ')[1]
                try:
                    token = jwt.decode(access_token, current_app.config['SECRET_KEY'])
                    current_user = User.find_by_username(token['uid'])
                    user_token = rj.jsonget(token['hash'], Path.rootPath())
                    if not user_token:
                        status = 401
                        message = TOKEN['revoked']
                        rest_api.abort()

                    if not current_user.is_verified:
                        status = 401
                        message = TOKEN['verified']
                        rest_api.abort()

                    if current_user.is_banned:
                        status = 401
                        message = TOKEN['banned']
                        rest_api.abort()
                    if not current_user.is_active:
                        status = 401
                        message = TOKEN['notActive']
                        rest_api.abort()
                except jwt.ExpiredSignatureError as e:
                    raise e
                except jwt.DecodeError as e:
                    raise e
                except jwt.InvalidTokenError as e:
                    raise e
                except:
                    rest_api.abort(status, message)

            except IndexError:
                raise jwt.InvalidTokenError
        else:
            rest_api.abort(401, TOKEN['required'])
        return f(*args, **kwargs, current_user=current_user)

    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__
    return wrapper

def token_optional(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        current_user = None
        if auth_header:
            try:
                access_token = auth_header.split(' ')[1]
                try:
                    token = jwt.decode(access_token, current_app.config['SECRET_KEY'])
                    current_user = User.find_by_username(token['uid'])
                    user_token = rj.jsonget(token['hash'], Path.rootPath())
                    if not user_token:
                        current_user=None

                except jwt.ExpiredSignatureError as e:
                    return f(*args, **kwargs, current_user=None)
                    # raise e
                except (jwt.DecodeError, jwt.InvalidTokenError) as e:
                    return f(*args, **kwargs, current_user=None)
                    # raise e
                except:
                    rest_api.abort(401, TOKEN['unknown'])

            except IndexError:
                return f(*args, **kwargs, current_user=None)
                # raise jwt.InvalidTokenError
        else:
            return f(*args, **kwargs, current_user=None)
        return f(*args, **kwargs, current_user=current_user)

    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__
    return wrapper
