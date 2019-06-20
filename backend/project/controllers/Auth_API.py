from flask_restful import Resource, reqparse
from project.model.user import *
from flask_jwt_extended import (set_refresh_cookies,create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt,set_access_cookies,get_csrf_token)
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
from ..model import *
from ..model.order import *
import json
from ..database import db
from project import app,mail
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
from ..melipayamak import SendMessage
from flask_mail import Message
from definitions import (MAX_LOGIN_ATTEMPTS, MAX_ACTIVATION_ATTEMPTS, MAX_DEFFER_ACTIVATION_TIME,
 MAX_MESSAGES_SEND, MAX_AVAILABLE_MESSAGE_TIME,COUPONCODE,MAX_INVITOR_POLICY,
 SMS_BodyId_VER,SMS_BodyId_WEL,SMS_BodyId_FPS,SITE_PREFIX)
import string,random
from datetime import datetime,timedelta

parser_register = reqparse.RequestParser()
parser_register.add_argument('username', help = 'ورود نام کاربری ضروری است', required = True)
parser_register.add_argument('password', help = 'ورود رمز عبور ضروری است', required = True)
parser_register.add_argument('c_password', help = 'ورود تکرار رمز عبور ضروری است', required = True)
parser_register.add_argument('mobile', help = 'ورود شماره موبایل ضروری است', required = True)
# parser_register.add_argument('accept_roles', help = 'تایید مقررات سایت الزامی است', required = True)

parser_login = reqparse.RequestParser()
parser_login.add_argument('username', help = 'ورود نام کاربری ضروری است', required = True)
parser_login.add_argument('password', help = 'ورود رمز عبور ضروری است', required = True)
parser_login.add_argument('remember_me', required = False)
parser_login.add_argument('next')

parser_verify = reqparse.RequestParser()
parser_verify.add_argument('code', help = 'ورود کد فعالسازی الزامی است', required = True)

parser_forgot = reqparse.RequestParser()
parser_forgot.add_argument('mobile', help = 'ورود شماره موبایل ضروری است', required = True)

parser_change = reqparse.RequestParser()
parser_change.add_argument('old_password', help = 'ورود رمزعبور فعلی ضروری است', required = True)
parser_change.add_argument('new_password', help = 'ورود رمز عبور جدید ضروری است', required = True)
parser_change.add_argument('confirm_password', help = 'ورود تکرار رمز عبور جدید ضروری است', required = True)

# def can_access(f):
#     if not hasattr(f, 'access_control'):
#         return True
#     return _eval_access(**f.access_control) == AccessResult.ALLOWED

class UserRegistration(Resource):
    def post(self):
        parser_register.parse_args()
        data = request.get_json(force=True)

        if User.find_by_username(data['username'].lower()):
            return make_response(jsonify({"message":{"success":False,"field":"username","text":'نام کاربری مورد نظر شما ازقبل در سیستم تعریف شده است. لطفا نام کاربری دیگری انتخاب کنید'}}),400)

        if data['username'].isdigit():
            return make_response(jsonify({"message":{"success":False,"field":"username","text":'نام کاربری شما نمی تواند بصورت عدد باشد'}}),400)

        if len(data['username']) > 32 or len(data['username']) < 3:
            return make_response(jsonify({"message":{"success":False,"field":"username","text":'نام کاربری انتخاب شده باید حداقل ۳حرفی و یا حداکثر ۳۲ حرفی باشد.'}}),400)

        if len(data['password']) > 32 or len(data['password']) < 4:
            return make_response(jsonify({"message":{"success":False,"field":"password","text":'رمز عبور انتخابی شما باید حداقل ۴ وحداکثر ۳۲ کاراکتری باشد'}}),400)

        if(data['password']!=data['c_password']):
            return make_response(jsonify({"message":{"success":False,"field":"c_password","text": 'رمز عبور با تکرار آن مطابقت ندارد'}}),400)

        if User.find_by_mobile(data['mobile']):
            return make_response(jsonify({"message":{"success":False,"field":"mobile","text":'این شماره موبایل از قبل در سیستم موجود است'}}),400)

        if len(data['mobile']) > 13 or len(data['mobile']) < 11 or not data['mobile'].isdigit():
            return make_response(jsonify({"message":{"success":False,"field":"mobile","text":'شماره موبایل وارد شده معتبر نیست'}}),400)

        invitor = data.get("invitor", None)

        if invitor:
            if not User.find_by_username(data['invitor']):
                msg = "کاربری با کد معرفی مورد نظر شما وجود ندارد. لطفا کد معرف خود را بطور صحیح وارد کنید ویا این قسمت را خالی رها کنید. "
                return make_response(jsonify({"message":{"success":False,"field":"invitor","text":msg}}),400)

            if User.query.filter_by(invitor=data['invitor']).count() >= MAX_INVITOR_POLICY:
                msg = ".معرف شما از حداکثر تعداد معرفی شدگان خود استفاده کرده است" \
                +" دقت فرمایید که هرفرد تنها قادر به معرفی "+MAX_INVITOR_POLICY+" نفر است."
                return make_response(jsonify({"message":{"success":False,"field":"invitor","text":msg}}),400)

        try:
            new_user = User(data['username'].lower())
            new_user.username = data['username'].lower()
            new_user.mobile = data['mobile']
            new_user.password = User.generate_hash(data['password'])
            new_user.invitor = invitor
            new_user.save_to_db()

            # expires = timedelta(days=365)
            # access_token = create_access_token(identity = data['username'].lower(),expires_delta=expires)
            # refresh_token = create_refresh_token(identity = data['username'].lower(),expires_delta=expires)

            current_user = User.find_by_username(data['username'].lower())

            session['username'] = data['username'].lower()

            resp = jsonify({
                'message': 'Ready for verification for {}'.format(current_user.username),
                # 'access_token': access_token,
                # 'refresh_token': refresh_token
                })

            # login_user(current_user,remember=False)
            # set_refresh_cookies(resp, refresh_token)
            # set_access_cookies(resp, access_token)

            return make_response(resp,200)
        except Exception as e:
            return make_response(jsonify({"message":{"error" : str(e)}}), 500)
    def get(self):
        return make_response(jsonify({"message":"online resources register"}),404)

class UserLogin(Resource):
    def post(self):
        parser_login.parse_args()
        data = request.get_json(force=True)

        username = data['username'].lower()
        password = data['password']

        current_user = User.find_by_username(username)

        if not current_user:
            return make_response(jsonify({"message" :{"success":False,"field":"username","text":'کاربری با نام کاربری مورد نظر شما پیدا نشد'}}),400)

        if current_user.login_attempts == MAX_LOGIN_ATTEMPTS:
            current_user.is_verified = False
            current_user.is_banned = True
            current_user.is_active = False
            db.session.add(current_user)
            db.session.commit()
            msg = "حساب  کاربری شما موقتا به حالت تعلیق در آمد لطفا با پشتیبانی سایت تماس حاصل کنید"
            return make_response(jsonify({'message':{"success":False,"field":"banned","text": msg}}),401)

        if User.verify_hash(password, current_user.password):

            if current_user.is_banned:
                msg = "متاسفانه حساب کاربری شما در لیست سیاه قرار گرفته است"
                return make_response(jsonify({'message':{"success":False,"field":"blacklist","text": msg}}),401)

            if not current_user.is_verified:
                session['username'] = username
                msg = "حساب کاربری شما باید از طریق شماره همراه فعال سازی شود"
                return make_response(jsonify({'message':{"success":False,"field":"verification","text":msg}}),401)

            expires = timedelta(days=365)
            access_token = create_access_token(identity = current_user.username,expires_delta=expires,fresh=True)
            refresh_token = create_refresh_token(identity = current_user.username,expires_delta=expires)
            resp = jsonify({
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'access_csrf': get_csrf_token(access_token),
                'refresh_csrf': get_csrf_token(refresh_token)
                })

            # Set the JWT cookies in the response
            redirect_to_auction = False
            auction_id = 0

            if 'next' in data and "participate" in data['next'] :
                temp = data['next']
                auction_id = temp.split('/')[2]
                if(current_user.has_auction(int(auction_id))):
                    redirect_to_auction = True



            if redirect_to_auction:
                resp = jsonify({
                    'message': 'Logged in as {}'.format(current_user.username),
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'redirect_to_auction': redirect_to_auction,
                    'auction_id':auction_id,
                    'access_csrf': get_csrf_token(access_token),
                    'refresh_csrf': get_csrf_token(refresh_token)
                    })

            # create orders from session on login
            if "orders" in session:
                order_schema = OrderSchema(many=True)
                for order in session['orders']:
                    new_order = Order()
                    item = Item.query.get(order[0]['item']['id'])
                    saved_before = Order.query.filter_by(user_id=current_user.id).join(Item).filter_by(id=item.id).first()
                    if not saved_before:
                        #calculate price base on auction participation
                        total = int(order[0]['total'])
                        item_price = (item.price - item.discount) * total
                        discount_status = OrderDiscountStatus.REGULAR
                        discount = item.discount * total

                        auction = current_user.auctions.join(Item).filter_by(id = item.id).first()
                        if auction:
                            offer = Offer.query.join(Auction).filter_by(id=auction.id).order_by("offers.created_at DESC").first()
                            discount_status = OrderDiscountStatus.INAUCTION
                            if offer and offer.win:
                                item_price = offer.total_price
                                discount_status = OrderDiscountStatus.AUCTIONWINNER
                                total = 1
                                discount = item.price - offer.total_price
                            else:
                                userplan = current_user.user_plans.join(Auction).filter_by(id=auction.id).first()
                                auctionplan = AuctionPlan.query.filter_by(auction_id=auction.id).join(UserPlan).filter_by(id=userplan.id).first()
                                item_price = item.price - auctionplan.discount
                                total = 1
                                discount = auctionplan.discount

                        new_order.item = item
                        new_order.total_cost = item_price
                        new_order.total = total
                        new_order.status = OrderStatus.UNPAID
                        new_order.discount_status = discount_status
                        new_order.total_discount = discount
                        new_order.user = current_user;
                        db.session.add(new_order)
                        db.session.commit()
                session.pop('orders')

            # if 'remember_me' in data and data['remember_me']==True:
            #     login_user(current_user,remember=True)
            # else:
            #     login_user(current_user,remember=False)

            expire_date = timedelta(days=365)
            set_refresh_cookies(resp, refresh_token,expire_date)
            set_access_cookies(resp, access_token,expire_date)
            login_user(current_user,remember=True)
            return make_response(resp,200)
        else:
            current_user.login_attempts += 1
            db.session.add(current_user)
            db.session.commit()
            return make_response(jsonify({'message':{"success":False,"field":"password","text": 'رمز عبور شما نادرست است'}}),401)

    def get(self):
        return make_response(jsonify({"message":"online resources login"}),404)

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = Revoked(jti = jti)
            revoked_token.add()
            return make_response(jsonify({'message': 'Access token has been revoked'}),200)
        except Exception as e:
            return make_response(jsonify({'message':{ 'error' : str(e)}}), 500)

class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = Revoked(jti = jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500

class UserTokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        resp = jsonify({'access_token': access_token})
        resp = jsonify({
            'message': 'Token refreshed for {}'.format(current_user),
            'access_token': access_token,
            })
        set_access_cookies(resp, access_token)
        return make_response(resp,200)

class UserVerification(Resource):
    def put(self):
        if "username" in session:
            current_user = User.find_by_username(session['username'].lower())
            now = datetime.now()
            data = request.get_json(force=True)

            if 'last_send_time' not in session:
                session['last_send_time'] = now + timedelta(seconds=MAX_AVAILABLE_MESSAGE_TIME)

            if 'resend' in data and data['resend']:
                session['last_send_time'] = now + timedelta(seconds=MAX_AVAILABLE_MESSAGE_TIME)

            if (now - session['last_send_time']).seconds >= MAX_AVAILABLE_MESSAGE_TIME:
                if current_user.send_sms_attempts == MAX_MESSAGES_SEND :
                    msg = "حد اکثر تلاشهای شما جهت دریافت کد فعال سازی به اتمام رسیده است. لطفا جهت پیگیری با پشتیبانی سایت تماس حاصل کنید."
                    return make_response(jsonify({"message":{"success":False,"text":msg,"field":"policy"}}),400)

                current_user.activation_code = random.randint(100000,1000000)
                current_user.send_sms_attempts += 1
                current_user.verification_attempts = 0
                db.session.add(current_user)
                db.session.commit()
                session['last_send_time'] = datetime.now()

                message = "کاربر گرامی" \
                + '\n' + "کد تایید حساب کاربری شما " + current_user.activation_code + " است."\
                + '\n' + 'یونی بید'\
                + '\n' + ' www.unibid.ir'

                text = current_user.activation_code + ";" + str(MAX_AVAILABLE_MESSAGE_TIME)
                sms_response = SendMessage(current_user,"فعال سازی حساب کاربری",message,text,SMS_BodyId_VER)

                if sms_response['success']:
                    return make_response(jsonify({"remained_to_expire": MAX_AVAILABLE_MESSAGE_TIME,"send_attempts":MAX_MESSAGES_SEND - current_user.send_sms_attempts }),200)
                else:
                    msg = ""
                    if sms_response['status_code'] == -3:
                        msg = "شماره همراه شما در سیستم مخابرات تعریف نشده است لطفا جهت تصحیح شماره همراه حساب کاربری خود با پشتیبانی سایت تماس بگیرید"
                        return make_response(jsonify({"message":{"success":False,"text":msg,"field":"system_error"}}),400)
                    elif sms_response['status_code'] == -6:
                        msg = "ارسال پیام شما با یک خطای داخلی اوپراتور مواجه شده است. لطفا با پشتیبانی سایت تماس حاصل کنید"
                        return make_response(jsonify({"message":{"success":False,"text":msg,"field":"system_error"}}),400)
                    elif sms_response['status_code'] == 11:
                        msg = "در حال حاضر سیستم قادر به ارسال پیام به شماره همراه شما نمی باشد. لطفا جهت تصحیح شماره همراه با پشتیبانی سایت تماس حاصل کنید"
                        return make_response(jsonify({"message":{"success":False,"text":msg,"field":"system_error"}}),400)
                    else:
                        msg = "ارسال پیامک به دلیل اختلال در سیستم پنل پیامکی با مشکل مواجه شده است."\
                        + '\n' + 'برای فعال سازی حساب کاربری خود از طریق ایمیل اقدام کنید یا با پشتیبانی سایت تماس حاصل کنید'
                        return make_response(jsonify({"message":{"success":False,"text":msg,"field":"not_delivered"}}),400)

            return make_response(jsonify({"remained_to_expire": MAX_AVAILABLE_MESSAGE_TIME - (now - session['last_send_time']).seconds,"send_attempts":MAX_MESSAGES_SEND - current_user.send_sms_attempts }),200)

        msg = "توکن فعال سازی حساب در دسترس نیست. لطفا دوباره اقدام به ورود به سایت کنید."
        return make_response(jsonify({"message":{"success":False,"field":"retry_login","text":msg}}),400)

    def post(self):
        if "username" in session:
            current_user = User.find_by_username(session['username'].lower())

            data = parser_verify.parse_args()
            data = request.get_json(force=True)
            verify_code = data['code']
            now = datetime.now()

            if ((now - current_user.updated_at).seconds >= MAX_DEFFER_ACTIVATION_TIME) and (current_user.verification_attempts == MAX_ACTIVATION_ATTEMPTS):
                current_user.verification_attempts = 0
                db.session.add(current_user)
                db.session.commit()

            if current_user.verification_attempts == MAX_ACTIVATION_ATTEMPTS:
                msg = "حداکثر تلاش های شما در مدت اعتبار کد ارسالی به انجام رسیده است. لطفا مجددا کد فعال سازی خود را درخواست کنید."
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"policy"}}),400)

            if verify_code != current_user.activation_code:
                current_user.verification_attempts +=1
                db.session.add(current_user)
                db.session.commit()
                msg = "کد وارد شده معتبر نمی باشد"
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"invalid"}}),400)

            if (now - session['last_send_time']).seconds >= MAX_AVAILABLE_MESSAGE_TIME:
                msg = "کد وارد شده شما منقضی شده است"
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"expire"}}),400)

            current_user.is_verified = True
            current_user.send_sms_attempts = 0
            current_user.verification_attempts = 0
            current_user.login_attempts = 0
            current_user.is_active = True
            db.session.add(current_user)
            db.session.commit()

            welcome_notification = SiteNotification()
            welcome_notification.title = 'به سایت یونی بید خوش آمدید'
            welcome_notification.text = 'به وب سایت ما خوش آمدید. لحظاتی خوبی را در یونی بید برای شما آرزومندیم.'
            welcome_notification.sms = current_user.username +' عزیز٬ '\
            + '\n' + "حساب کاربری شما با موفقیت فعال سازی شد." \
            + '\n' + "با آرزوی موفقیت و شادکامی شما"\
            + '\n' + 'یونی بید'\
            + '\n' + 'www.unibid.ir'
            welcome_notification.link = SITE_PREFIX
            welcome_notification.details = current_user.username
            welcome_notification.type = SiteNotificationType.WELCOME
            welcome_notification.user = current_user
            db.session.add(welcome_notification)
            db.session.commit()

            expires = timedelta(days=365)
            access_token = create_access_token(identity =  session['username'].lower(),expires_delta=expires)
            refresh_token = create_refresh_token(identity =  session['username'].lower(),expires_delta=expires)

            msg = "حساب کاربری شما با موفقیت فعال شد. لطفا جهت بهبود خدمات نسبت به تکمیل پروفایل کاربری خود اقدام کنید."

            resp = jsonify({
                'text': msg,
                'access_token': access_token,
                'refresh_token': refresh_token
                })

            login_user(current_user,remember=False)
            set_refresh_cookies(resp, refresh_token)
            set_access_cookies(resp, access_token)

            del session['last_send_time']
            del session['username']
            return make_response(resp,200)

        msg = "توکن فعال سازی حساب در دسترس نیست. لطفا دوباره اقدام به ورود به سایت کنید."
        return make_response(jsonify({"message":{"success":False,"field":"retry_login","text":msg}}),400)

    def get(self):
        resp = {
            "message_ttl":MAX_AVAILABLE_MESSAGE_TIME,
        }
        return make_response(jsonify(resp),200)

class UserVerificationMail(Resource):
    def put(self):
        if "username" in session:

            data = request.get_json(force=True)
            email = data.get("email", None)
            if not email:
                msg = "ورود پست الکترونیکی معتبر ضروری است"
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"email"}}),400)

            current_user = User.find_by_username(session['username'].lower())
            now = datetime.now()
            current_user.activation_code = random.randint(100000,1000000)
            current_user.verification_attempts = 0
            db.session.add(current_user)
            db.session.commit()

            message = Message("ارسال کد فعال سازی یونی بید",sender=("یونی بید", "info@unibid.ir"))
            message.add_recipient(email)
            token = User.generate_hash(current_user.username)
            message.html = render_template('site/mail.html',activation_code=current_user.activation_code,activation_token=token)
            # "فعال سازی حساب کاربری یونی بید" \
            # + '\n' + "کدفعال سازی حساب کاربری شما :" \
            # + '\n' + current_user.activation_code \
            # + '\n' + 'با آرزوی سلامتی و شادکامی برای شما'\
            # + '\n' + 'تیم یونی بید www.unibid.ir'

            mail.send(message)
            current_user.email = email
            db.session.add(current_user)
            db.session.commit()

            msg = "یک ایمیل حاوی کد فعال سازی به آدرس پست الکترونیکی شما ارسال شد"
            return make_response(jsonify({"message":{"success":True,"text":msg,"field":"delivered"}}),200)


        msg = "توکن فعال سازی حساب در دسترس نیست. لطفا دوباره اقدام به ورود به سایت کنید."
        return make_response(jsonify({"message":{"success":False,"field":"retry_login","text":msg}}),400)
    def post(self):
        if "username" in session:
            current_user = User.find_by_username(session['username'].lower())
            data = request.get_json(force=True)
            verify_code = data.get("code", None)

            if not verify_code:
                msg = "ورود کد فعال سازی جهت اعتبار سنجی حساب کاربری ضروری است."
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"email"}}),400)

            now = datetime.now()

            if current_user.verification_attempts == MAX_ACTIVATION_ATTEMPTS:
                msg = "حداکثر تلاش های شما در مدت اعتبار کد ارسالی به انجام رسیده است. لطفا مجددا کد فعال سازی خود را درخواست کنید."
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"policy"}}),400)

            if verify_code != current_user.activation_code:
                current_user.verification_attempts +=1
                db.session.add(current_user)
                db.session.commit()
                msg = "کد وارد شده معتبر نمی باشد"
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"invalid"}}),400)

            current_user.is_verified = True
            current_user.send_sms_attempts = 0
            current_user.verification_attempts = 0
            current_user.login_attempts = 0
            current_user.is_active = True
            db.session.add(current_user)
            db.session.commit()

            message = Message("فعال سازی حساب کاربری یونی بید",sender=("یونی بید", "info@unibid.ir"))
            message.add_recipient(current_user.email)
            message.html = render_template('site/verified.html')

            # "فعال سازی حساب کاربری یونی بید" \
            # + '\n' + current_user.username + " عزیز !"\
            # + '\n' + "حساب کاربری شما با موفقیت فعال سازی شد" \
            # + '\n' + 'ساعات خوشی را برای شما در سایت یونی بید آرزومندیم'\
            # + '\n' + 'تیم یونی بید www.unibid.ir'

            mail.send(message)

            welcome_notification = SiteNotification()
            welcome_notification.title = 'به سایت یونی بید خوش آمدید'
            welcome_notification.text = 'به وب سایت ما خوش آمدید. لحظاتی خوبی را در یونی بید برای شما آرزومندیم.'
            welcome_notification.sms = current_user.username +' عزیز٬ '\
            + '\n' + "حساب کاربری شما با موفقیت فعال سازی شد." \
            + '\n' + 'www.unibid.ir'
            welcome_notification.link = SITE_PREFIX
            welcome_notification.details = current_user.username
            welcome_notification.type = SiteNotificationType.WELCOME
            welcome_notification.user = current_user
            db.session.add(welcome_notification)
            db.session.commit()

            expires = timedelta(days=365)
            access_token = create_access_token(identity =  session['username'].lower(),expires_delta=expires,fresh=True)
            refresh_token = create_refresh_token(identity =  session['username'].lower(),expires_delta=expires)

            msg = "حساب کاربری شما با موفقیت فعال شد. لطفا جهت بهبود خدمات نسبت به تکمیل پروفایل کاربری خود اقدام کنید."

            resp = jsonify({
                'text': msg,
                'access_token': access_token,
                'refresh_token': refresh_token
                })

            set_refresh_cookies(resp, refresh_token)
            set_access_cookies(resp, access_token)
            login_user(current_user,remember=False)

            del session['last_send_time']
            del session['username']
            return make_response(resp,200)

        msg = "توکن فعال سازی حساب در دسترس نیست. لطفا دوباره اقدام به ورود به سایت کنید."
        return make_response(jsonify({"message":{"success":False,"field":"retry_login","text":msg}}),400)

class UserForgotPassword(Resource):
    def get(self):
        pass
    def post(self):
        parser_forgot.parse_args()

        data = request.get_json(force=True)
        mobile = data.get("mobile", None)

        if User.query.filter_by(mobile=mobile).count() > 1:
            msg = "بیش از یک کاربر با این شماره موبایل در سیستم ثبت شده اند. لطفا جهت پیگیری موضوع با پشتیبانی سایت تماس حاصل کنید."
            return make_response(jsonify({"message":{"success":False,"text":msg,"field":"mobile"}}),400)

        current_user = User.find_by_mobile(mobile)
        if not current_user :
            msg = "کاربری با شماره موبایل وارد شده در سیستم تعریف نشده است"
            return make_response(jsonify({"message":{"success":False,"text":msg,"field":"mobile"}}),400)

        if current_user.send_sms_attempts == MAX_MESSAGES_SEND :
            msg = "حداکثر تلاشهای شما جهت دریافت رمز یکبار مصرف انجام گرفته است. لطفا با پشتیبانی سایت تماس حاصل کنید"
            return make_response(jsonify({"message":{"success":False,"text":msg,"field":"policy"}}),400)

        new_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        current_user.password =User.generate_hash(new_password)
        current_user.send_sms_attempts += 1
        db.session.add(current_user)
        db.session.commit()
        session['last_send_time'] = datetime.now()

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
            msg = "یک پیام متنی حاوی رمز عبور یکبارمصرف برای شما پیامک شد که به وسیله آن می توانید جهت ورود به سایت اقدام کنید."
            return make_response(jsonify({"message":{"success" : True,"text":msg,"field":"password_sent"}}),200)
        else:
            msg = ""
            if sms_response['status_code'] == -3:
                msg = "شماره همراه شما در سیستم مخابرات تعریف نشده است لطفا جهت تصحیح شماره همراه حساب کاربری خود با پشتیبانی سایت تماس بگیرید"
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"password_not_sent"}}),400)
            elif sms_response['status_code'] == -6:
                msg = "ارسال پیام شما با یک خطای داخلی اوپراتور مواجه شده است. لطفا با پشتیبانی سایت تماس حاصل کنید"
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"password_not_sent"}}),400)
            elif sms_response['status_code'] == 11:
                msg = "در حال حاضر سیستم قادر به ارسال پیام به شماره همراه شما نمی باشد. لطفا جهت تصحیح شماره همراه با پشتیبانی سایت تماس حاصل کنید"
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"password_not_sent"}}),400)
            else:
                msg = "ارسال پیامک به دلیل اختلال در سیستم پنل پیامکی با مشکل مواجه شده است."
                return make_response(jsonify({"message":{"success":False,"text":msg,"field":"password_not_sent"}}),400)

        msg = "مشکلی در ارسال رمزعبور شما به شماره همراه اعلام شده در سیستم به وجود آمد. لطفا با پشتیبانی سایت تماس حاصل فرایید"
        return make_response(jsonify({"message":{"success" : False,"text":msg,"field":"password_not_sent"}}),400)

class UserChangePassword(Resource):
    @jwt_required
    def post(self):
        parser_change.parse_args()
        data = request.get_json(force=True)

        if not User.verify_hash(data['old_password'], current_user.password):
            return make_response(jsonify({"message":{"success":False,"field":"password","text":'رمز عبور فعلی شما نادرست است'}}),400)


        if len(data['new_password']) > 32 or len(data['new_password']) < 4:
            return make_response(jsonify({"message":{"success":False,"field":"password","text":'رمز عبور جدید شما باید حداقل ۴ و حداکثر ۳۲ کاراکتری باشد'}}),400)

        if(data['new_password']!=data['confirm_password']):
            return make_response(jsonify({"message":{"success":False,"field":"password","text":'تکرار رمزعبور جدید شما با رمز عبور جدید مطابقت ندارد'}}),400)

        current_user.password = User.generate_hash(data['new_password'])
        db.session.add(current_user)
        db.session.commit()

        message = current_user.username +' عزیز٬ '\
        + '\n' + 'شما در تاریخ ' + data['current_time'] + ' نسبت به تغییر رمز عبور خود در یونی بید اقدام کرده اید.'\
        + '\n' + 'www.unibid.ir'

        changepass_notification = SiteNotification()
        changepass_notification.title = 'تغییر رمز عبور'
        changepass_notification.text = 'رمز عبور شما تغییر یافت. برای دسترسی به همه امکانات لطفا دوباره به یونی بید وارد شوید'
        changepass_notification.sms = message
        changepass_notification.link = SITE_PREFIX+'/logout'
        changepass_notification.details = current_user.username+";"+data['current_time']
        changepass_notification.type = SiteNotificationType.CHANGEPASS
        changepass_notification.user = current_user
        db.session.add(changepass_notification)
        db.session.commit()

        return make_response(jsonify({"message":{"success":False,"field":"relogin","text":'رمزعبور شما با موفقیت تغییر کرد.لطفا با استفاده از رمزعبور جدید به سایت وارد شوید.'}}),200)
