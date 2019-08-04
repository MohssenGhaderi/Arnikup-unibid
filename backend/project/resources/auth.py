from flask_restplus import Resource, fields, Namespace
from flask import current_app, request, abort, make_response , jsonify , session
from ..model import *
import json
from ..database import db
from project import app,mail, rest_api, redis_db , rj
from ..melipayamak import SendMessage
from flask_mail import Message
from definitions import (MAX_LOGIN_ATTEMPTS, MAX_ACTIVATION_ATTEMPTS, MAX_DEFFER_ACTIVATION_TIME,
 MAX_MESSAGES_SEND, MAX_AVAILABLE_MESSAGE_TIME,COUPONCODE,MAX_INVITOR_POLICY,
 SMS_BodyId_VER,SMS_BodyId_WEL,SMS_BodyId_FPS,SITE_PREFIX)
import string,random
from datetime import datetime,timedelta
from project.lang.fa import *
from project.utils import token_required, token_optional
import jwt
import hashlib
from rejson import Path
from sqlalchemy import func


auth_ns = Namespace('auth')

login_fields = auth_ns.model('Login', {
    'username': fields.String(description='The login username', required=True,min_length=3,max_length=32),
    'password': fields.String(description='The login password', required=True,min_length=4,max_length=32),
})

register_fields = auth_ns.model('Register', {
    'username': fields.String(description='The register username', required=True,min_length=3,max_length=32),
    'password': fields.String(description='The register password', required=True,min_length=4,max_length=32),
    'confirmPassword': fields.String(description='The register confirm password', required=True,min_length=4,max_length=32),
    'mobile': fields.String(description='The user mobile field', required=True,min_length=11,max_length=11),
    'invitor': fields.String(description='The user invitor field',min_length=3,max_length=32),
})

verify_fields = auth_ns.model('Verify', {
    'code': fields.String(description='The user verification code', required=True,min_length=6,max_length=6),
})

verify_resend_fields = auth_ns.model('Resend', {
    'resend': fields.Boolean(description='The user resend verification code', required=True),
})

forgotpass_fields = auth_ns.model('ForgotPassword', {
    'forgotField': fields.String(description='The forgot field must be username or mobile', required=True,min_length=3,max_length=32),
})

changepass_fields = auth_ns.model('ChangePassword', {
    'oldPassword': fields.String(description='old user password', required=True,min_length=4,max_length=32),
    'newPassword': fields.String(description='new user password', required=True,min_length=4,max_length=32),
    'confirmPassword': fields.String(description='confirm new password', required=True,min_length=4,max_length=32),
    'currentTime': fields.String(description='current user friendly client time', required=True),
})

return_token_model = auth_ns.model('ReturnToken', {
    'accessToken': fields.String(required=True),
    'refreshToken': fields.String(required=True)
})

verification_attempts_fields = auth_ns.model('VerificationAttempts',{
    'remainedToExpire':fields.Integer(required=True),
    'sendAttempts':fields.Integer(required=True),
})

@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.response(200, 'User registered successfully and is waiting for verification')
    @auth_ns.response(400, 'Validation Error')
    @auth_ns.expect(register_fields,validate=False)
    def post(self):

        required_fields = ['username','password','confirmPassword','mobile']
        for key in required_fields:
            if key not in auth_ns.payload:
                for k, v in REGISTER_REQUIRED.items():
                    if key==k:
                        return make_response(jsonify({"success":False,"reason":k,"message":v}),400)

        username = auth_ns.payload['username'].lower()
        password = auth_ns.payload['password']
        c_password = auth_ns.payload['confirmPassword']
        mobile = auth_ns.payload['mobile']

        if User.find_by_username(username):
            return make_response(jsonify({"success":False,"reason":'username',"message":USER_ALREADY_REGISTERED}),400)

        if str(username).isdigit():
            return make_response(jsonify({"success":False,"reason":'username',"message":USER_NAME_MUST_STRING}),400)


        if len(username) > 32 or len(username) < 3:
            return make_response(jsonify({"success":False,"reason":'username',"message":USER_NAME_LENGTH}),400)

        if len(password) > 32 or len(password) < 4:
            return make_response(jsonify({"success":False,"reason":'password',"message":PASSWORD['LENGTH']}),400)

        if(password != c_password):
            return make_response(jsonify({"success":False,"reason":'confirmPassword',"message":PASSWORD['SAME']}),400)

        if not str(mobile).isdigit():
            return make_response(jsonify({"success":False,"reason":'mobile',"message":MOBILE_MUST_NUMBER}),400)

        if len(mobile) > 13 or len(mobile) < 11:
            return make_response(jsonify({"success":False,"reason":'mobile',"message":MOBILE_NOT_CORRECT}),400)

        if username in BANNED_USER_NAMES:
            return make_response(jsonify({"success":False,"reason":'username',"message":BANNED_USER_NAME}),400)

        for item in BANNED_USER_NAMES:
            if item in username and username not in BANNED_EXCEPTION_USER_NAMES:
                return make_response(jsonify({"success":False,"reason":'username',"message":BANNED_USER_NAME}),400)

        if User.find_by_mobile(mobile):
            return make_response(jsonify({"success":False,"reason":'mobile',"message":MOBILE_ALREADY_EXIST}),400)

        invitor = None
        if 'invitor' in auth_ns.payload:
            invitor = auth_ns.payload['invitor'].lower()

            if not User.find_by_username(invitor):
                return make_response(jsonify({"success":False,"reason":"invitor","message":INVITOR_NOT_EXIST}),400)

            if User.query.filter_by(invitor=invitor).count() >= MAX_INVITOR_POLICY:
                return make_response(jsonify({"success":False,"reason":"invitor","message":INVITOR_MAX}),400)

        new_user = User(username)
        new_user.username = username
        new_user.mobile = mobile
        new_user.password = User.generate_hash(password)
        new_user.invitor = invitor
        for avatar in Avatar.query.filter_by(type=AvatarType.REGULAR):
            new_user.avatars.append(avatar)

        avatar = Avatar.query.filter_by(type=AvatarType.REGULAR).order_by(func.random()).first()
        new_user.avatar = avatar
        new_user.level = Level.query.filter_by(number=1).first()
        new_user.save_to_db()

        current_user = User.find_by_username(username)

        user_agent_string = request.user_agent.string.encode('utf-8')
        user_agent_hash = hashlib.md5(user_agent_string).hexdigest()
        obj = {
            'username': current_user.username,
            'code_expiration_time': None
        }
        rj.jsonset(user_agent_hash, Path.rootPath(), obj)

        resp ={
            'message': 'Ready for verification for {}'.format(current_user.username),
            'username': username
        }
        return make_response(jsonify(resp),200)

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.response(200, "Success",return_token_model)
    @auth_ns.response(403, 'System Policy')
    @auth_ns.response(401, 'Not Authorized')
    @auth_ns.response(400, 'Validation Error')
    @auth_ns.expect(login_fields,validate=False)

    def post(self):

        required_fields = ['username','password']
        for key in required_fields:
            if key not in auth_ns.payload:
                for k, v in REGISTER_REQUIRED.items():
                    if key==k:
                        return make_response(jsonify({"success":False,"reason":k,"message":v}),400)

        if('username' not in auth_ns.payload or 'password' not in auth_ns.payload):
            return make_response(jsonify({"success":False,"reason":"username","message":USER_NAME_PASS_NOT_FOUND}),400)

        username = auth_ns.payload['username'].lower()
        password = auth_ns.payload['password']

        if str(username).isdigit():
            return make_response(jsonify({"success":False,"reason":"username","message":USER_NAME_MUST_STRING}),400)
        if len(username) > 32 or len(username) < 3:
            return make_response(jsonify({"success":False,"reason":"username","message":USER_NAME_LENGTH}),400)
        if len(password) > 32 or len(password) < 4:
            return make_response(jsonify({"success":False,"reason":"username","message":PASSWORD['LENGTH']}),400)

        current_user = User.find_by_username(username)
        if not current_user:
            return make_response(jsonify({"success":False,"reason":"username","message":USER_NOT_FOUND}),400)

        if current_user.login_attempts == MAX_LOGIN_ATTEMPTS:
            current_user.is_verified = False
            current_user.is_banned = True
            current_user.is_active = False
            db.session.add(current_user)
            db.session.commit()
            return make_response(jsonify({"success":False,"reason":"banned","message": BANNED_USER_MAX_LOGIN_ATTEMPTS}),403)

        if User.verify_hash(password, current_user.password):

            if current_user.is_banned:
                return make_response(jsonify({"success":False,"reason":"banned","message": BANNED_USER}),403)

            user_agent_string = request.user_agent.string.encode('utf-8')
            user_agent_hash = hashlib.md5(user_agent_string).hexdigest()
            obj = {
                'username': current_user.username,
                'code_expiration_time': None,
                'avatar':current_user.avatar.image.split("'")[1]
            }
            rj.jsonset(user_agent_hash, Path.rootPath(), obj)


            if not current_user.is_verified:

                ua = UserActivity()
                ua.user = current_user
                ua.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
                ua.activity = ACTIVITIES['NOT_VERIFIED_LOGIN']
                db.session.add(ua)
                db.session.commit()

                return make_response(jsonify({"success":False,"reason":"verification","message":MUST_VERIFIED}),403)
            # jwt operations

            _access_token = jwt.encode({'hash': user_agent_hash,
                                        'uid': current_user.username,
                                        'exp': datetime.utcnow() + timedelta(seconds=current_app.config['ONLINE_USER_ACCESS_TIME']),
                                        'iat': datetime.utcnow()},
                                       current_app.config['SECRET_KEY']).decode('utf-8')

            _refresh_token = jwt.encode({'hash': user_agent_hash,
                                         'exp': datetime.utcnow() + timedelta(seconds=current_app.config['ONLINE_USER_REFRESH_TIME']),
                                         'iat': datetime.utcnow()},
                                        current_app.config['SECRET_KEY']).decode('utf-8')

            now = int(time.time())
            expires = now + (current_app.config['ONLINE_USER_REFRESH_TIME']) + 10
            p = redis_db.pipeline()
            p.expireat(user_agent_hash, expires)
            p.execute()

            ua = UserActivity()
            ua.user = current_user
            ua.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            ua.activity = ACTIVITIES['LOGIN']
            db.session.add(ua)
            db.session.commit()

            return make_response(jsonify({'accessToken': _access_token, 'refreshToken': _refresh_token}),200)

        else:
            ua = UserActivity()
            ua.user = current_user
            ua.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            ua.activity = ACTIVITIES['ATTEMPT']
            db.session.add(ua)
            current_user.login_attempts += 1
            db.session.add(current_user)
            db.session.commit()

            return make_response(jsonify({"success":False,"reason":"password","message":USER_WRONG_PASSWORD}),403)

@auth_ns.route('/verify')
class Verify(Resource):
    @auth_ns.response(200, 'Success',return_token_model)
    @auth_ns.response(400, 'Validation Error')
    @auth_ns.response(401, 'System Policy Error')
    @auth_ns.response(403, 'Not authorized or token not available')
    @auth_ns.expect(verify_fields,validate=False)

    def post(self):
        user_agent_string = request.user_agent.string.encode('utf-8')
        user_agent_hash = hashlib.md5(user_agent_string).hexdigest()
        username = rj.jsonget(user_agent_hash, Path('.username'))

        if username:
            current_user = User.find_by_username(username)
            required_fields = ['code']
            for key in required_fields:
                if key not in auth_ns.payload:
                    for k, v in VERIFICATION_CODEـREQUIRED.items():
                        if key==k:
                            return make_response(jsonify({"success":False,"reason":k,"message":v}),400)
            verify_code = auth_ns.payload['code']
            now = datetime.now()
            if ((now - current_user.updated).seconds >= MAX_DEFFER_ACTIVATION_TIME) and (current_user.verification_attempts == MAX_ACTIVATION_ATTEMPTS):
                current_user.verification_attempts = 0
                db.session.add(current_user)
                db.session.commit()

            if current_user.verification_attempts == MAX_ACTIVATION_ATTEMPTS:
                return make_response(jsonify({"success":False,"reason":'verifyCodeMaxAttemptMeet',"message":VERIFICATION_CODE_MAX_ATTEMPT}),403)

            if verify_code != current_user.activation_code:
                current_user.verification_attempts +=1
                db.session.add(current_user)
                db.session.commit()
                return make_response(jsonify({"success":False,"reason":'wrongVerifyCode',"message":VERIFICATION_CODE_WRONG}),403)

            code_expiration_time_str = rj.jsonget(user_agent_hash, Path('.code_expiration_time'))
            code_expiration_time = datetime.strptime(code_expiration_time_str, '%Y-%m-%d %H:%M:%S.%f')

            if (code_expiration_time - now).seconds >= MAX_AVAILABLE_MESSAGE_TIME:
                return make_response(jsonify({"success":False,"reason":'expireVerifyCode',"message":VERIFICATION_CODE_EXPIRED}),403)

            current_user.is_verified = True
            current_user.send_sms_attempts = 0
            current_user.verification_attempts = 0
            current_user.login_attempts = 0
            current_user.is_active = True
            db.session.add(current_user)
            db.session.commit()

            welcome_notification = SiteNotification()
            welcome_notification.title = MESSAGES['welcome_title']
            welcome_notification.text = MESSAGES['welcome_desc']
            welcome_notification.sms = current_user.username + MESSAGES['welcome_sms']
            welcome_notification.link = SITE_PREFIX
            welcome_notification.details = current_user.username
            welcome_notification.type = SiteNotificationType.WELCOME
            welcome_notification.user = current_user
            db.session.add(welcome_notification)
            db.session.commit()

            ua = UserActivity()
            ua.user = current_user
            ua.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            ua.activity = ACTIVITIES['LOGIN_AFTER_VERIFY']
            db.session.add(ua)
            db.session.commit()

            rj.jsondel(user_agent_hash)

            user_agent_string = request.user_agent.string.encode('utf-8')
            user_agent_hash = hashlib.md5(user_agent_string).hexdigest()

            _access_token = jwt.encode({'hash': user_agent_hash,
                                        'uid': current_user.username,
                                        'exp': datetime.utcnow() + timedelta(seconds=current_app.config['ONLINE_USER_ACCESS_TIME']),
                                        'iat': datetime.utcnow()},
                                       current_app.config['SECRET_KEY']).decode('utf-8')

            _refresh_token = jwt.encode({'hash': user_agent_hash,
                                         'exp': datetime.utcnow() + timedelta(seconds=current_app.config['ONLINE_USER_REFRESH_TIME']),
                                         'iat': datetime.utcnow()},
                                        current_app.config['SECRET_KEY']).decode('utf-8')
            obj = {
                'username': current_user.username,
                'code_expiration_time': None
            }
            rj.jsonset(user_agent_hash, Path.rootPath(), obj)

            now = int(time.time())
            expires = now + (current_app.config['ONLINE_USER_REFRESH_TIME']) + 10
            p = redis_db.pipeline()
            p.expireat(user_agent_hash, expires)
            p.execute()

            return make_response(jsonify({'accessToken': _access_token, 'refreshToken': _refresh_token}),200)

        return make_response(jsonify({"success":False,"reason":'retryLogin',"message":VERIFICATION_TOKEN_MISSED}),403)

    @auth_ns.response(200, 'Success',verification_attempts_fields)
    @auth_ns.response(400, 'SMS Validation Error')
    @auth_ns.response(401, 'Not Authorized')
    @auth_ns.response(403, 'Not authorized or token not available')
    @auth_ns.expect(verify_resend_fields,validate=False)

    def put(self):
        user_agent_string = request.user_agent.string.encode('utf-8')
        user_agent_hash = hashlib.md5(user_agent_string).hexdigest()
        username = rj.jsonget(user_agent_hash, Path('.username'))

        if username:
            current_user = User.find_by_username(username)
            if not current_user :
                return make_response(jsonify({"success":False,"reason":'username',"message":USER_NOT_FOUND}),403)

            now = datetime.now()
            code_expiration_time = now + timedelta(seconds=MAX_AVAILABLE_MESSAGE_TIME)

            code_expiration_time_str = rj.jsonget(user_agent_hash, Path('.code_expiration_time'))

            if not code_expiration_time_str or ('resend' in auth_ns.payload and auth_ns.payload['resend']):
                rj.jsonset(user_agent_hash, Path('.code_expiration_time'), str(code_expiration_time))
            else:
                code_expiration_time = datetime.strptime(code_expiration_time_str, '%Y-%m-%d %H:%M:%S.%f')

            if (code_expiration_time - now).seconds >= MAX_AVAILABLE_MESSAGE_TIME:
                if current_user.send_sms_attempts == MAX_MESSAGES_SEND :
                    rj.jsonset(user_agent_hash, Path('.username'),None)
                    return make_response(jsonify({"success":False,"reason":'maxVerificationRetryReached',"message":MAX_VERIFICATION_RETRY_REACHED}),403)

                current_user.activation_code = random.randint(100000,1000000)
                current_user.send_sms_attempts += 1
                current_user.verification_attempts = 0
                db.session.add(current_user)
                db.session.commit()
                code_expiration_time = now + timedelta(seconds=MAX_AVAILABLE_MESSAGE_TIME)
                rj.jsonset(user_agent_hash, Path('.code_expiration_time'), str(code_expiration_time))

                message = "کاربر گرامی" \
                + '\n' + "کد تایید حساب کاربری شما " + current_user.activation_code + " است."\
                + '\n' + 'یونی بید'\
                + '\n' + ' www.unibid.ir'

                text = current_user.activation_code + ";" + str(MAX_AVAILABLE_MESSAGE_TIME)
                sms_response = SendMessage(current_user,"فعال سازی حساب کاربری",message,text,SMS_BodyId_VER)
                print (sms_response)

                if sms_response['success']:
                    return make_response(jsonify({"remainedToExpire": MAX_AVAILABLE_MESSAGE_TIME,"sendAttempts":MAX_MESSAGES_SEND - current_user.send_sms_attempts }),200)
                else:
                    if sms_response['status_code'] == -3:
                        return make_response(jsonify({"success":False,"reason":'smsError',"message":SMS_ERRORS['UNDEFINED_NUMBER']}),400)
                    elif sms_response['status_code'] == -6:
                        return make_response(jsonify({"success":False,"reason":'smsError',"message":SMS_ERRORS['INNER_ERROR']}),400)
                    elif sms_response['status_code'] == 11:
                        return make_response(jsonify({"success":False,"reason":'smsError',"message":SMS_ERRORS['WRONG_NUMBER']}),400)
                    else:
                        return make_response(jsonify({"success":False,"reason":'smsError',"message":SMS_ERRORS['SYSTEM_ERROR']}),400)

            return make_response(jsonify({"remainedToExpire": (code_expiration_time - now).seconds,"sendAttempts":MAX_MESSAGES_SEND - current_user.send_sms_attempts }),200)

        return make_response(jsonify({"success":False,"reason":'retryLogin',"message":VERIFICATION_TOKEN_MISSED}),403)

    @auth_ns.response(200, 'Verification code time to live')
    def get(self):
        pass
        # return make_response(jsonify({"verificationTTL":MAX_AVAILABLE_MESSAGE_TIME}),200)

@auth_ns.route('/password/forgot')
class ForgotPassword(Resource):
    @auth_ns.response(200, 'Success')
    @auth_ns.response(400, 'SMS System and Validation Error')
    @auth_ns.response(401, 'Not Authorized')
    @auth_ns.response(403, 'Not available')
    @auth_ns.expect(forgotpass_fields, validate= False)
    def post(self):
        data = request.get_json(force=True)

        if 'forgotField' not in auth_ns.payload:
            return make_response(jsonify({"success":False,"reason":'forgotField',"message":MOBILE_OR_USERNAME_REQUIRED}),400)

        current_user = User.query.filter_by(username=auth_ns.payload['forgotField'].lower()).first()
        if not current_user :
            current_user = User.query.filter_by(mobile=auth_ns.payload['forgotField']).first()
            if not current_user :
                return make_response(jsonify({"success":False,"reason":'userNotFound',"message":USER_NOT_FOUND}),403)

        if not current_user.mobile:
            return make_response(jsonify({"success":False,"reason":'user.mobile',"message":MOBILE_NOT_FOUND}),403)

        mobile = current_user.mobile

        if not str(mobile).isdigit():
            return make_response(jsonify({"success":False,"reason":'mobile',"message":MOBILE_MUST_NUMBER}),400)

        if len(mobile) > 13 or len(mobile) < 11:
            return make_response(jsonify({"success":False,"reason":'mobile',"message":MOBILE_NOT_CORRECT}),400)

        if User.query.filter_by(mobile=mobile).count() > 1:
            return make_response(jsonify({"success":False,"reason":'mobile',"message":MOBIL_REAPETED}),403)

        current_user = User.find_by_mobile(mobile)
        if not current_user :
            return make_response(jsonify({"success":False,"reason":'mobile',"message":MOBILE_NOT_FOUND}),403)

        if current_user.send_sms_attempts == MAX_MESSAGES_SEND :
            return make_response(jsonify({"success":False,"reason":'mobile',"message":PASSWORD_SENT_MAX}),403)

        new_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        current_user.password =User.generate_hash(new_password)
        current_user.send_sms_attempts += 1
        db.session.add(current_user)
        db.session.commit()
        
        message = current_user.username +' عزیز٬ '\
        + '\n' + "رمز عبور جدید شما :" + new_password + "است."\
        + '\n' + 'www.unibid.ir'

        text = current_user.username+";"+new_password
        sms_response = SendMessage(current_user,'فراموشی رمزعبور',message,text,SiteNotificationType.FORGOTPASS)

        forgotpass_notification = SiteNotification()
        forgotpass_notification.title = 'فراموشی رمز عبور'
        forgotpass_notification.text = 'یک رمز عبور جدید با فرایند فراموشی رمزعبور برای شما پیامک شد. لطفا در اولین ورود به سایت نسبت به تغییر رمز عبور خود اقدام کنید.'
        forgotpass_notification.sms = message
        forgotpass_notification.link = SITE_PREFIX
        forgotpass_notification.details = current_user.username+";"+new_password
        forgotpass_notification.type = SiteNotificationType.FORGOTPASS
        forgotpass_notification.delivered = sms_response['success']
        forgotpass_notification.user = current_user
        db.session.add(forgotpass_notification)
        db.session.commit()

        if sms_response['success']:
            return make_response(jsonify({"success":True,"reason":'passwordSent',"message":FORGOT_PASSWORD_SENT}),200)
        else:
            if sms_response['status_code'] == -3:
                return make_response(jsonify({"success":False,"reason":'passwordNotSent',"message":SMS_ERRORS['UNDEFINED_NUMBER']}),400)
            elif sms_response['status_code'] == -6:
                return make_response(jsonify({"success":False,"reason":'passwordNotSent',"message":SMS_ERRORS['INNER_ERROR']}),400)
            elif sms_response['status_code'] == 11:
                return make_response(jsonify({"success":False,"reason":'passwordNotSent',"message":SMS_ERRORS['WRONG_NUMBER']}),400)
            else:
                return make_response(jsonify({"success":False,"reason":'passwordNotSent',"message":SMS_ERRORS['SYSTEM_ERROR']}),400)
        return make_response(jsonify({"success":False,"reason":'passwordProblem',"message":FORGOT_PASSWORD_PROBLEM}),400)

@auth_ns.route('/password/change')
class ChangePassword(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @auth_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @auth_ns.doc('Change password api.', parser=parser, body=changepass_fields, validate=False)
    @auth_ns.response(200, 'Success')
    @auth_ns.response(400, 'SMS System and Validation Error')
    @auth_ns.response(401, 'Not Authorized')
    @auth_ns.response(403, 'Not available')
    @token_required
    def post(self,current_user):

        required_fields = ['oldPassword','newPassword','confirmPassword','currentTime']
        for key in required_fields:
            if key not in auth_ns.payload:
                for k, v in CHANGEPASS_REQUIRED.items():
                    if key==k:
                        return make_response(jsonify({"success":False,"reason":k,"message":v}),400)

        if len(auth_ns.payload['newPassword']) < 4:
            return make_response(jsonify({"success":False,"reason":'newPassword',"message":PASS_VALIDATION['min_length']}),400)

        if len(auth_ns.payload['newPassword']) > 32:
            return make_response(jsonify({"success":False,"reason":'newPassword',"message":PASS_VALIDATION['max_length']}),400)

        if(auth_ns.payload['newPassword']!=auth_ns.payload['confirmPassword']):
            return make_response(jsonify({"success":False,"reason":'confirmPassword',"message":PASS_VALIDATION['same']}),400)

        if not User.verify_hash(auth_ns.payload['oldPassword'], current_user.password):
            return make_response(jsonify({"success":False,"reason":"password","message":PASSWORD['FAILED']}),400)


        current_user.password = User.generate_hash(auth_ns.payload['newPassword'])
        db.session.add(current_user)
        db.session.commit()

        message = current_user.username +' عزیز٬ '\
        + '\n' + 'شما در تاریخ ' + auth_ns.payload['currentTime'] + ' نسبت به تغییر رمز عبور خود در یونی بید اقدام کرده اید.'\
        + '\n' + 'www.unibid.ir'

        changepass_notification = SiteNotification()
        changepass_notification.title = 'تغییر رمز عبور'
        changepass_notification.text = 'رمز عبور شما تغییر یافت. برای دسترسی به همه امکانات لطفا دوباره به یونی بید وارد شوید'
        changepass_notification.sms = message
        changepass_notification.link = SITE_PREFIX+'/logout'
        changepass_notification.details = current_user.username+";"+auth_ns.payload['currentTime']
        changepass_notification.type = SiteNotificationType.CHANGEPASS
        changepass_notification.user = current_user
        db.session.add(changepass_notification)
        db.session.commit()

        return make_response(jsonify({"success":True,"reason":"relogin","message":PASSWORD['CHANGE']}),200)


@auth_ns.route('/refresh')
class Refresh(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token',required=False)
    @rest_api.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @rest_api.doc(parser=parser,validate=True)
    @auth_ns.expect(rest_api.model('RefreshToken', {'refreshToken': fields.String(required=True)}), validate=True)
    @auth_ns.response(200, 'Success', return_token_model)
    def post(self):
        auth_header = request.headers.get('Authorization')

        try:
            if auth_header:
                _refresh_token = auth_header.split(' ')[1]
                token = jwt.decode(_refresh_token, current_app.config['SECRET_KEY'])
                user_hash = redis_db.get(token['hash'])

                if not user_hash:
                    raise jwt.InvalidIssuerError

                # Generate new pair

                user_agent_string = request.user_agent.string.encode('utf-8')
                user_agent_hash = hashlib.md5(user_agent_string).hexdigest()

                _access_token = jwt.encode({'uid': user_hash.decode('utf-8'),
                                            'exp': datetime.utcnow() + timedelta(seconds=current_app.config['ONLINE_USER_ACCESS_TIME']),
                                            'iat': datetime.utcnow()},
                                           current_app.config['SECRET_KEY']).decode('utf-8')

                _refresh_token = jwt.encode({'hash': user_agent_hash,
                                             'exp': datetime.utcnow() + timedelta(seconds=current_app.config['ONLINE_USER_REFRESH_TIME']),
                                             'iat': datetime.utcnow()},
                                            current_app.config['SECRET_KEY']).decode('utf-8')

                now = int(time.time())
                expires = now + (current_app.config['ONLINE_USER_REFRESH_TIME']) + 10
                p = redis_db.pipeline()
                p.expireat(user_agent_hash, expires)
                p.execute()

                return make_response(jsonify({'accessToken': _access_token, 'refreshToken': _refresh_token}),200)
            else:
                return make_response(jsonify({'success': False, 'reason': 'missing authorization headers'}),401)

        except jwt.ExpiredSignatureError as e:
            raise e
        except (jwt.DecodeError, jwt.InvalidTokenError)as e:
            raise e
        except:
            auth_ns.abort(401, 'Unknown token error')

@auth_ns.route('/logout')
class Logout(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @auth_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @auth_ns.doc('Logout api.', parser=parser, validate=True)
    @auth_ns.response(200, 'Success')
    @token_required
    def post(self,current_user):
        ua = UserActivity()
        ua.user = current_user
        ua.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        ua.activity = ACTIVITIES['LOGOUT']
        db.session.add(ua)
        db.session.commit()
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(' ')[1]
        token = jwt.decode(access_token, current_app.config['SECRET_KEY'])
        p = redis_db.pipeline()
        p.delete(token['hash'])
        p.execute()
        return make_response(jsonify({"success":True,"reason":"logout"}),200)

@auth_ns.route('/avatar')
class Avatar(Resource):
    def get(self):
        user_agent_string = request.user_agent.string.encode('utf-8')
        user_agent_hash = hashlib.md5(user_agent_string).hexdigest()
        avatar = rj.jsonget(user_agent_hash, Path('.avatar'))
        return make_response(jsonify(avatar),200)
