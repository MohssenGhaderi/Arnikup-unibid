from project.database import db
from project.model import *
from definitions import BASE_BID_PRICE
from flask import current_app, url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app, socketio, rj
from datetime import datetime , timedelta
import time
from flask_socketio import emit, join_room, leave_room
from flask_jwt_extended import jwt_required
from sqlalchemy import or_ , and_ , asc , desc
from project.lang.fa import *
import functools
import jwt
from rejson import Path
from project.helpers import *
import math
from definitions import AUCTION_START_PROGRESS
from threading import Thread

def authenticated(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        arguments = dict(*args)
        if 'authorization' in arguments:
            access_token = arguments['authorization'].strip()
            reason = 'unknown'
            message = TOKEN['unknown']
            current_user = None
            error = True
            try:
                token = jwt.decode(access_token, current_app.config['SECRET_KEY'])
                current_user = User.query.filter_by(username=token['uid']).first()
                error = False
                user_token = rj.jsonget(token['hash'], Path.rootPath())
                if not user_token:
                    reason = 'revoked'
                    message = TOKEN['revoked']
                    error = True

                if not current_user.is_verified:
                    reason = 'verified'
                    message = TOKEN['verified']
                    error = True


                if current_user.is_banned:
                    reason = 'banned'
                    message = TOKEN['banned']
                    error = True


                if not current_user.is_active:
                    reason = 'notActive'
                    message = TOKEN['notActive']
                    error = True

            except jwt.ExpiredSignatureError as e:
                reason = 'expired'
                message = TOKEN['expired']
                error = True

            except jwt.DecodeError as e:
                reason = 'decode'
                message = TOKEN['decode']
                error = True

            except jwt.InvalidTokenError as e:
                reason = 'issue'
                message = TOKEN['issue']
                error = True

            except jwt.exceptions.InvalidSignatureError as e:
                reason = 'malformed'
                message = TOKEN['malformed']
                error = True

            except:
                reason = 'unknown'
                message = TOKEN['unknown']

            if error:
                return emit("failed",{"error":{"message":message,"reason":reason,"status":401}})
            else:
                return f(*args, **kwargs,current_user=current_user)
        else:
            return emit("failed",{"error":{"message":TOKEN['required'],"reason":'tokenRequired',"status":401}}),
    return wrapped
