from flask_restful import Resource, reqparse
import os
from os import listdir
from os.path import isfile, join
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session, flash
import json
from project import app
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
from ..model.user_message import UserMessage
from ..model.user_gift import *
from ..model.order import *
from werkzeug.utils import secure_filename
from ..utils import Payload
from definitions import COUPONCODE,MAX_INVITOR_POLICY,MAXIMUM_ORDERS,MESSAGE_SUBJECTS,AVATAR_DIR,MAX_MESSAGE_POLICY,SITE_PREFIX
import copy
import random
from datetime import datetime
from flask_jwt_extended import JWTManager,jwt_required,jwt_refresh_token_required
from sqlalchemy import or_ , and_
from ..melipayamak import SendMessage


parser_user_message = reqparse.RequestParser()
parser_user_message.add_argument('subject', help = 'ورود موضوع پیام ضروری است', required = True)
parser_user_message.add_argument('title', help = 'ورود عنوان پیام ضروری است', required = True)
parser_user_message.add_argument('message', help = 'متنی برای پیام وارد نکرده اید', required = True)

parse_payment_account = reqparse.RequestParser()
parse_payment_account.add_argument('first_name', help = 'ورود نام ضروری است', required = True)
parse_payment_account.add_argument('last_name', help = 'ورود نام خانوادگی ضروری است', required = True)
parse_payment_account.add_argument('state', help = 'ورود استان ضروری است', required = True)
parse_payment_account.add_argument('city', help = 'ورود شهر ضروری است', required = True)
parse_payment_account.add_argument('address', help = 'ورود آدرس ضروری است', required = True)
parse_payment_account.add_argument('mobile', help = 'ورود شماره همراه ضروری است', required = True)
parse_payment_account.add_argument('accept_tick', required = False)
parse_payment_account.add_argument('work_place', required = False)
parse_payment_account.add_argument('postal_code',help='ورود کد پستی ضروری است',required = True)
parse_payment_account.add_argument('more_info', required = False)
parse_payment_account.add_argument('email', required = False)
parse_payment_account.add_argument('shipment_method',help='ورود روش ارسال الزامی است', required = True)
parse_payment_account.add_argument('payment_method',help='ورود روش پرداخت الزامی است', required = True)



class PaymentsInfo(Resource):
    @jwt_required
    def get(self,pagenum,pagesize):
        result = Payment.query.filter_by(user_id=current_user.id).order_by('created_at DESC').limit(pagesize)
        payments = []
        for payment in result:
            orders = []
            plan = None
            if (payment.type == PaymentType.PRODUCT):
                order_result = Order.query.filter_by(payment_id=payment.id).all()
                shipment = None
                for order in order_result:
                    shipment_result = Shipment.query.filter_by(order_id=order.id).first()
                    if shipment_result:
                        shipment={
                        "method":shipment_result.shipment_method.title,
                        "status":shipment_result.status,
                        "send_date":shipment_result.send_date,
                        }
                    orders.append({
                    "title":order.item.title,
                    "total":order.total,
                    "main_price":str(order.item.price),
                    "total_price":str(order.total * order.item.price),
                    "discount":str(order.total_discount),
                    "paid":str(order.total * order.item.price - order.total_discount),
                    "shipment":shipment,
                    })
            elif payment.type==PaymentType.PLAN:
                unpaid_user_plan = UserPlan.query.filter_by(payment_id=payment.id, user_id = current_user.id).first()
                if unpaid_user_plan:

                    state = "عدم شرکت درحراجی"
                    if payment.status == PaymentStatus.ARCHIVE:
                        state = "شرکت کننده حراجی"

                    plan={
                    "title":unpaid_user_plan.auction_plan.plan.title,
                    "price":str(unpaid_user_plan.auction_plan.price),
                    "discount":str(unpaid_user_plan.auction_plan.discount),
                    "offers":unpaid_user_plan.auction_plan.max_offers,
                    "state":state,
                    }
            messages = []
            for message in payment.messages:
                messages.append({
                "title":message.title,
                "message":message.message,
                "date":message.created_at,
                })
            payments.append({
            "GUID":payment.GUID,
            "amount":str(payment.amount),
            "date":payment.created_at,
            "type":payment.type,
            "status":payment.status,
            "method":payment.payment_method.title,
            "plan":plan,
            "orders":orders,
            "messages":messages,
            })
        return make_response(jsonify(payments),200)

class UserBasicInfo(Resource):
    @jwt_required
    def get(self):
        user = User.query.get(current_user.id)
        userSchema = UserSchema()
        return make_response(jsonify(userSchema.dump(user)),200)

    # @jwt_required
    # def post(self):
    #     # json_data = request.get_json(force=True)
    #
    #     user_data = parser_user_account.parse_args()
    #
    #     current_user.alias_name = request.form.get('alias-name')
    #     current_user.first_name = request.form.get('first-name')
    #     current_user.last_name = request.form.get('last-name')
    #     current_user.work_place = request.form.get('work-place')
    #     current_user.mobile = user_data['mobile']
    #     current_user.email = user_data('email')
    #
    #
    #
    #     if(not current_user.address):
    #         address = Address()
    #         address.city = address_data['city']
    #         address.address = address_data['address']
    #         state = State.query.get(address_data['state'])
    #         address.state = state
    #         address.postal_code = address_data['postal_code']
    #         try:
    #             db.session.add(address)
    #             db.session.commit()
    #             current_user.address = address
    #         except Exception as e:
    #             return make_response(jsonify({"message": e.message}), 500)
    #     else:
    #         current_user.address.city = address_data['city']
    #         current_user.address.address = address_data['address']
    #         state = State.query.get(address_data['state'])
    #         current_user.address.state = state
    #         current_user.address.postal_code = address_data['postal_code']
    #
    #     avatar_index = request.form.get('avatar-index',None)
    #     if(avatar_index):
    #         current_user.avatar = "['"+request.form.get('avatar-index')+"']"
    #
    #     old_password = request.form.get('current-password',None)
    #     new_password = request.form.get('password',None)
    #     repeat_password = request.form.get('c_password',None)
    #
    #     if new_password :
    #         if not User.verify_hash(old_password, current_user.password):
    #             msg = " رمز عبور قبلی شما نادرست است"
    #             return  make_response(jsonify({"message":{"error":msg}}),403)
    #
    #         if new_password != repeat_password:
    #             msg = "رمز عبور جدید با تکرار رمز عبور همخوانی ندارد"
    #             return make_response(jsonify({"message": {"confirm-password":msg}}),403)
    #
    #         current_user.password = User.generate_hash(new_password)
    #
    #     #handle invitor copun code
    #     invitor_code = request.form.get('invitor-code',None)
    #
    #     if(invitor_code):
    #
    #         invitor = User.query.filter_by(username=invitor_code).first()
    #
    #         if(not invitor):
    #             msg ="کد معرف مورد نظر موجود نمی باشد"
    #             return make_response(jsonify({"message":{"error":msg}}),500)
    #         if(invitor.id == current_user.id):
    #             msg ="شما قادر به معرفی خود نیستید"
    #             return make_response(jsonify({"message":{"error":msg}}),500)
    #
    #         already_invited = current_user.gifts.filter_by(title=COUPONCODE).first()
    #
    #         if(already_invited):
    #             msg = "جایزه کد معرفی شما قبلا استفاده شده است"
    #             return make_response(jsonify({"message":{"error":msg}}),400)
    #
    #         invitor_count = User.query.filter_by(invitor=invitor_code).count
    #
    #         if User.query.filter_by(invitor=invitor_code).count() >= MAX_INVITOR_POLICY:
    #             msg = "تعداد افراد معرفی شده توسط " + invitor_code + " به پایان رسیده است."
    #             return make_response(jsonify({"message":{"error":msg}}),400)
    #
    #         gift = Gift.query.filter_by(title=COUPONCODE).first()
    #         current_user.gifts.append(gift)
    #         current_user.credit += Decimal(gift.amount)
    #         current_user.invitor = invitor.username
    #         invitor.credit += Decimal(gift.amount)
    #         db.session.add(invitor)
    #         db.session.commit()
    #
    #     try:
    #         db.session.add(current_user)
    #         db.session.commit()
    #         msg = " اطلاعات شما با موفقیت ذخیره شد "
    #         if new_password :
    #             logout_user()
    #         return make_response(jsonify({"message":{"success":msg}}),200)
    #     except Exception as e:
    #         return make_response(jsonify({"message":{"error":e.message}}), 500)

class UserInformation(Resource):
    @jwt_required
    def get(self):
        if not current_user.is_authenticated:
            msg ="برای استفاده از این اطلاعات باید لاگین کنید"
            return make_response(jsonify({"message":{"success":False,'type':"login",'text':msg}}),500)

        credit = current_user.credit
        enrolled_auctions = UserAuctionParticipation.query.filter_by(user_id=current_user.id).count()

        invitations = User.query.filter_by(invitor=current_user.username).count()

        bought_items = Order.query.filter_by(user_id = current_user.id, status=OrderStatus.PAID).count()

        won_offers = Offer.query.filter_by(win=True).join(UserPlan).filter_by(user_id = current_user.id).all()

        won_auctions = [auction for offer in won_offers for auction in Auction.query.filter_by(id=offer.auction_id)]

        # won_items_in_auction = [Item.query.filter_by(id=auction.item_id) for auction in won_auctions]

        total_discount = 0
        for auction in won_auctions:
            item = Item.query.filter_by(id = auction.item_id).first()
            offer = Offer.query.filter_by(auction_id = auction.id, win=True).first()
            total_discount += item.price - offer.total_price

        states = []
        for state in State.query.order_by('title').distinct().all():
            states.append({
            "id":state.id,
            "title":state.title
            })

        avatars = []
        for root, dirs, files in os.walk(AVATAR_DIR):
            for filename in files:
                avatars.append({"name":filename})
        user_address = None
        if current_user.address:
            user_address = {
            "state":current_user.address.state.id,
            "city":current_user.address.city,
            "address":current_user.address.address,
            "postal_code":int(current_user.address.postal_code),
            }

        user_info = {
        "credit":str(current_user.credit),
        "username":current_user.username,
        "alias_name":current_user.alias_name,
        "first_name":current_user.first_name,
        "last_name":current_user.last_name,
        "work_place":current_user.work_place,
        "email":current_user.email,
        "mobile":current_user.mobile,
        "avatar":current_user.avatar[2:-2]
        }

        messages = []
        for message in current_user.messages:
            messages.append({
            "title":message.title,
            "date":message.created_at,
            "message":message.message,
            "subject":message.subject,
            })

        result = {
            "total_discount": int(total_discount),
            "won_auctions": len(won_offers),
            "total_boughts": bought_items,
            "total_enrolled_auctions": enrolled_auctions,
            "total_invitations": invitations,
            "invitation_code": current_user.username,
            "states":states,
            "user_information":user_info,
            "avatars":avatars,
            "message_subjects":MESSAGE_SUBJECTS,
            "messages":messages,
            "user_address":user_address,
        }
        return make_response(jsonify(result),200)

    @jwt_required
    def post(self):
        if not current_user.is_authenticated:
            msg ="برای استفاده از این اطلاعات باید لاگین کنید"
            return make_response(jsonify({"message":{"success":False,'type':"login",'text':msg}}),500)

        user_data = request.get_json(force=True)
        user_mobile = user_data.get("mobile", None)

        if not user_mobile:
            msg ="ورود شماره همراه ضروری است"
            return make_response(jsonify({"message":{"success":False,'type':"mobile",'text':msg}}),400)

        if user_mobile!=current_user.mobile and User.find_by_mobile(user_mobile):
            msg ="کاربری با این شماره همراه از قبل در سیستم تعریف شده است. اگر قادر به اصلاح شماره همراه خودتان نیستید با پشتیبانی تماس حاصل فرمایید."
            return make_response(jsonify({"message":{"success":False,'type':"mobile",'text':msg}}),400)

        current_user.alias_name = user_data.get("alias_name", None)
        current_user.first_name = user_data.get("first_name", None)
        current_user.last_name = user_data.get("last_name", None)
        current_user.work_place = user_data.get("work_place", None)
        current_user.email = user_data.get("email", None)

        user_state = user_data.get("state", None)
        user_city = user_data.get("city", None)
        user_address = user_data.get("address", None)
        user_postal_code = user_data.get("postal_code", None)

        if not user_state:
            msg ="ورود استان ضروری است"
            return make_response(jsonify({"message":{"success":False,'type':"state",'text':msg}}),400)

        if not user_city:
            msg ="ورود شهر محل سکونت ضروری است"
            return make_response(jsonify({"message":{"success":False,'type':"city",'text':msg}}),400)

        if not user_address:
            msg ="ورود آدرس دقیق پستی ضروری است"
            return make_response(jsonify({"message":{"success":False,'type':"address",'text':msg}}),400)

        if not user_postal_code:
            msg ="ورود کد پستی ضروری است"
            return make_response(jsonify({"message":{"success":False,'type':"postal_code",'text':msg}}),400)

        if not (str(user_postal_code)).isdigit():
            msg ="کدپستی باید بصورت عددی باشد"
            return make_response(jsonify({"message":{"success":False,'type':"postal_code",'text':msg}}),400)

        if len(str(user_postal_code)) < 10 or len(str(user_postal_code)) > 11:
            msg ="کد پستی باید ۱۰ رقمی باشد"
            return make_response(jsonify({"message":{"success":False,'type':"postal_code",'text':msg}}),400)

        if(not current_user.address):
            address = Address()
            address.city = user_city
            address.address = user_address
            address.state = State.query.get(user_state)
            address.postal_code = user_postal_code
            try:
                db.session.add(address)
                db.session.commit()
                current_user.address = address
            except Exception as e:
                return make_response(jsonify({"message":{'success':False,'text':e.message}}),500)
        else:
            current_user.address.city = user_city
            current_user.address.address = user_address
            current_user.address.state = State.query.get(user_state)
            current_user.address.postal_code = user_postal_code

        avatar = user_data.get("avatar", None)
        if avatar:
            avatars = []
            for root, dirs, files in os.walk(AVATAR_DIR):
                for filename in files:
                    avatars.append(filename)

            if(avatar in avatars):
                current_user.avatar = "['"+avatar+"']"

        #handle invitor copun code
        # invitor_code = user_data.get("invitor", None)

        # if(invitor_code):
        #     msg ="عملیات کد دعوت از این بخش فعلا غیر فعال است"
        #     return make_response(jsonify({"message":{"success":False,'text':msg}}),400)
        #
        #     invitor = User.query.filter_by(username=invitor_code).first()
        #
        #     if(not invitor):
        #         msg ="کد معرف مورد نظر موجود نمی باشد"
        #         return make_response(jsonify({"message":{"error":msg}}),400)
        #     if(invitor.id == current_user.id):
        #         msg ="شما قادر به معرفی خود نیستید"
        #         return make_response(jsonify({"message":{"error":msg}}),400)
        #
        #     already_invited = current_user.gifts.filter_by(title=COUPONCODE).first()
        #
        #     if(already_invited):
        #         msg = "جایزه کد معرفی شما قبلا استفاده شده است"
        #         return make_response(jsonify({"message":{"error":msg}}),400)
        #
        #     if User.query.filter_by(invitor=invitor_code).count() >= MAX_INVITOR_POLICY:
        #         msg = ".معرف شما از حداکثر تعداد معرفی شدگان خود استفاده کرده است" \
        #         + " دقت فرمایید که هرفرد تنها قادر به معرفی "+MAX_INVITOR_POLICY+" نفر است."
        #
        #         return make_response(jsonify({"message":{"error":msg}}),400)
        #
        #         gift = Gift.query.filter_by(title=COUPONCODE).first()
        #         if not gift:
        #             msg = "جایزه معرفی کاربران در سیستم تعریف نشده است"
        #             return make_response(jsonify({"message":{"error":msg}}),400)
        #
        #         if gift and not gift.expired:
        #             current_user.gifts.append(gift)
        #             current_user.credit += gift.amount
        #             db.session.add(current_user)
        #             db.session.commit()
        #             invitor = User.query.filter_by(username=current_user.invitor).first()
        #             if invitor:
        #                 invitor.credit += gift.amount
        #                 db.session.add(invitor)
        #                 db.session.commit()
        #
        #     gift = Gift.query.filter_by(title=COUPONCODE).first()
        #     if gift:
        #         user_gift = db.session.query(user_gifts).filter_by(user_id=current_user.id, gift_id=gift.id,used=True).first()
        #         if(user_gift):
        #             msg = "جایزه کد معرفی شما قبلا استفاده شده است"
        #             return make_response(jsonify({"message":{"error":msg}}),400)
        #         else:
        #             current_user.gifts.append(gift)
        #             current_user.credit += gift.amount
        #             current_user.invitor = invitor.username
        #             invitor.credit += gift.amount
        #             db.session.add(invitor)
        #             db.session.add(current_user)
        #             db.session.commit()
        #             # update extra field for relationship
        #             stmt = user_gifts.update().where(and_(user_gifts.c.user_id==current_user.id,user_gifts.c.gift_id==gift.id)).values(used=True)
        #             db.engine.execute(stmt)

        # try:
        if current_user.mobile!=str(user_mobile):
            current_user.mobile = user_data.get("mobile", None)
            current_user.is_verified = False
            current_user.verification_attempts = 0
            current_user.send_sms_attempts = 0
            db.session.add(current_user)
            db.session.commit()
            logout_user()
            msg = "تغییرات موردنظر شما با موفقیت اعمال شد. به دلیل اعلام شماره همراه جدید جهت انجام مجدد اعتبار سنجی خود از سیستم خارج می شوید!"
            return make_response(jsonify({"message":{"success":True,'field':"relogin",'text':msg}}),200)
        else:
            db.session.add(current_user)
            db.session.commit()
            msg = " اطلاعات شما با موفقیت ذخیره شد "
            return make_response(jsonify({"message":{"success":True,'text':msg}}),200)

        # except Exception as e:
        #     return make_response(jsonify({"message":{"success":False,'text':e.message}}), 500)

class UserContactUs(Resource):

    def _allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in definitions.ALLOWED_EXTENTIONS

    @jwt_required
    def post(self):
        user_message = parser_user_message.parse_args()
        if len(current_user.messages) >= MAX_MESSAGE_POLICY:
            msg ="حداکثر پیام های شما ارسال شده است"
            return make_response(jsonify({"message":{"success":False,"text":msg}}),400)


        new_message = UserMessage()
        new_message.title = user_message['title']
        new_message.subject = user_message['subject']
        new_message.message = user_message['message']
        new_message.user = current_user

        if 'file' in request.files:
            file = request.files['file']
            if file and self._allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                new_message.file = path
            else:
                msg ="نوع فایل انتخابی شما مناسب نمی باشد"
                return make_response(jsonify({"message":{"success":{"error":msg}}}),400)

        db.session.add(new_message)
        db.session.commit()
        msg ="پیام شما با موفقیت ارسال شد. در اولین فرصت جهت پیگیری با شما تماس خواهیم گرفت"
        return make_response(jsonify({"message":{"success":True,"text":msg}}),200)
        # flash("پیام با موفقیت ارسال شد")
        # return redirect(url_for('profile'))

parser = reqparse.RequestParser()
parser.add_argument('item_id')

class UserCartOrder(Resource):
    def calculate_response(self):
        result = Order.query.filter(or_(Order.status==OrderStatus.UNPAID, Order.status==OrderStatus.PAYING)).filter_by(user_id=current_user.id).order_by('created_at DESC')
        orders = []
        for order in result:
            title = order.item.product.title
            if (len(title) > 20):
                title = title[:20]+"..."
            item_title = order.item.title
            if (len(item_title) > 50):
                item_title = item_title[:50]+"..."
            product_title = order.item.product.title
            if (len(product_title) > 50):
                product_title = product_title[:50]+"..."
            fulltitle = product_title + " - " + item_title
            discounted_price = 0

            if order.discount_status == OrderDiscountStatus.REGULAR:
                discounted_price = order.item.discount * order.total

            elif order.discount_status == OrderDiscountStatus.INAUCTION :
                auction = current_user.auctions.join(Item).filter_by(id = order.item.id).order_by('auctions.created_at DESC').first()
                userplan = current_user.user_plans.join(Auction).filter_by(id=auction.id).first()
                auctionplan = AuctionPlan.query.filter_by(auction_id=auction.id).join(UserPlan).filter_by(id=userplan.id).first()
                if auctionplan:
                    discounted_price = auctionplan.discount

            elif order.discount_status == OrderDiscountStatus.AUCTIONWINNER:
                auction = current_user.auctions.join(Item).filter_by(id = order.item.id).order_by('auctions.created_at DESC').first()
                offer = Offer.query.filter_by(auction_id=auction.id,win=True).first()
                if offer:
                    discounted_price = order.item.price - offer.total_price

            orders.append({
            "id" : order.id,
            "item_id" : order.item.id,
            "title" : title,
            "item_title" : item_title,
            "product_title" : product_title,
            "fulltitle" : product_title + " - " + item_title,
            "images" : order.item.images,
            "main_price" : str(order.total * order.item.price),
            "discounted_price" : str(order.total * order.item.price - discounted_price),
            "quantity" : order.item.quantity,
            "total" : order.total,
            "status" : order.status,
            "discount_status" : order.discount_status,
            })
        return orders

    def get(self):
        if current_user.is_authenticated:
            return make_response(jsonify(self.calculate_response()), 200)
        else:
            if "orders" in session:
                return make_response(jsonify(session['orders']), 200)
            else:
                return make_response(jsonify({"msg": "no orders"}), 200)

    def post(self):
        order_schema = OrderSchema(many=True)
        data = request.get_json(force=True)
        item_id = int(data.get("item_id", None))
        total = int(data.get("total", None))
        item = Item.query.get(item_id)

        if current_user.is_authenticated:
            last_order = Order.query.filter_by(user_id=current_user.id,item_id=item_id,status=OrderStatus.UNPAID).first()
            if(last_order):
                msg = "این محصول رو قبلا به سبد خرید اضافه کرده اید"
                return make_response(jsonify({"reason":msg}),400)

            last_paid_order = Order.query.filter_by(user_id=current_user.id,item_id=item_id,status=OrderStatus.PAID).first()


            #calculate price base on auction participation
            item_price = (item.price - item.discount) * total
            discount_status = OrderDiscountStatus.REGULAR
            discount = item.discount * total

            auction = current_user.auctions.join(Item).filter_by(id = item.id).first()
            if auction and not last_paid_order:
                offer = Offer.query.join(Auction).filter_by(id=auction.id).order_by("offers.created_at DESC").first()
                if offer and offer.user_plan.user.id==current_user.id and offer.win:
                    item_price = offer.total_price
                    discount_status = OrderDiscountStatus.AUCTIONWINNER
                    total = 1
                    discount = item.price - offer.total_price
                else:
                    auction = current_user.auctions.join(Item).filter_by(id = item.id).order_by('auctions.created_at DESC').first()
                    userplan = current_user.user_plans.join(Auction).filter_by(id=auction.id).first()
                    auctionplan = AuctionPlan.query.filter_by(auction_id=auction.id).join(UserPlan).filter_by(id=userplan.id).first()
                    discount = auctionplan.discount
                    total = 1
                    item_price = item.price - auctionplan.discount
                    discount_status = OrderDiscountStatus.INAUCTION

                    # auctionplan = AuctionPlan.query.filter_by(auction_id=auction.id).join(UserPlan).filter_by(user_id=current_user.id).first()
                    # discount_status = OrderDiscountStatus.INAUCTION
                    # item_price = item.price - auctionplan.discount
                    # total = 1
                    # discount = auctionplan.discount

            new_order = Order()
            new_order.user = current_user
            new_order.item = item
            new_order.total_cost = item_price
            new_order.discount_status = discount_status
            new_order.status = OrderStatus.UNPAID
            new_order.total = total
            new_order.total_discount = discount
            db.session.add(new_order)
            db.session.commit()

            return make_response(jsonify(self.calculate_response()), 200)
        else:

            if not "orders" in session:
                session['orders'] = []

            founded = False
            order_schema = OrderSchema(many=True)
            founded = next((x for x in session['orders'] if x[0]['item']['id'] == item.id and (x[0]['status'] == OrderStatus.UNPAID or x[0]['status'] == OrderStatus.PAYING)), None)
            if (founded):
                msg = "این محصول رو قبلا به سبد خرید اضافه کرده اید"
                return make_response(jsonify({"reason":msg}),400)

            if len(session['orders']) < MAXIMUM_ORDERS :
                new_order = Order()
                new_order.id = random.randint(1,1000)
                new_order.item = item;
                new_order.total_cost = (item.price - item.discount) * total
                new_order.total = total
                new_order.status = OrderStatus.UNPAID
                new_order.discount_status = OrderDiscountStatus.REGULAR
                new_order.total_discount = item.discount * total
                order_schema = OrderSchema()
                session['orders'].append(order_schema.dump(new_order))
                return make_response(jsonify(session['orders']), 200)
            else:
                return make_response(jsonify({"reason": "حداکثر تعداد سبد خرید شما پر شده است"}), 400)

    def patch(self):
        data = request.get_json(force=True)
        order_id = int(data.get("order_id", None))
        total = int(data.get("total", None))

        if current_user.is_authenticated:
            new_order = Order.query.get(order_id)
            item = new_order.item
            #calculate price base on auction participation
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

            new_order.total_cost = item_price
            new_order.status = OrderStatus.UNPAID
            new_order.discount_status = discount_status
            new_order.total = total
            new_order.total_discount = discount
            db.session.add(new_order)
            db.session.commit()

            return make_response(jsonify(self.calculate_response()), 200)
        else:
            order = next((x for x in session['orders'] if x[0]['id'] == order_id),None)

            if ((order[0]['status'] == str(OrderStatus.UNPAID) or order[0]['status'] == str(OrderStatus.PAYING))):
                order[0]['total_cost'] = (order[0]['item']['price'] - order[0]['item']['discount']) * total
                order[0]['total'] = total
                order[0]['total_discount'] = order[0]['item']['discount'] * total

                return make_response(jsonify(session['orders']), 200)

    def delete(self):
        data = request.get_json(force=True)
        order_id = int(data.get("order_id", None))
        print ("order_id for delete",order_id)
        if current_user.is_authenticated:
            print ("auth cart for delete",order_id)
            Order.query.filter_by(id=order_id).delete()
            db.session.commit()

            if len(current_user.orders) == 0:
                for gift in current_user.gifts:
                    user_gift = db.session.query(user_gifts).filter_by(user_id=current_user.id, gift_id=gift.id).first()
                    if not user_gift.used:
                        current_user.gifts.remove(gift)

            db.session.commit()

            return make_response(jsonify(self.calculate_response()), 200)

        else:
            order = None
            for x in session['orders']:
                if x[0]['id'] == order_id:
                    order = x
                    break
            # order = next(x for x in session['orders'] if x[0]['id'] == order_id)
            if order:
                session['orders'].remove(order)
            return make_response(jsonify(session['orders']), 200)

class UserCartCheckout(Resource):
    @jwt_required
    def get(self):
        if current_user.is_authenticated:
            result = Order.query.filter_by(user_id=current_user.id,status=OrderStatus.PAYING).order_by('created_at DESC')
            orders = []
            for order in result:
                title = order.item.product.title
                if (len(title) > 20):
                    title = title[:20]+"..."
                item_title = order.item.title
                if (len(item_title) > 50):
                    item_title = item_title[:50]+"..."
                product_title = order.item.product.title
                if (len(product_title) > 50):
                    product_title = product_title[:50]+"..."
                fulltitle = product_title + " - " + item_title
                discounted_price = 0

                if order.discount_status == OrderDiscountStatus.REGULAR:
                    discounted_price = order.item.discount * order.total

                elif order.discount_status == OrderDiscountStatus.INAUCTION :
                    auction = current_user.auctions.join(Item).filter_by(id = order.item.id).order_by('auctions.created_at DESC').first()
                    userplan = current_user.user_plans.join(Auction).filter_by(id=auction.id).first()
                    auctionplan = AuctionPlan.query.filter_by(auction_id=auction.id).join(UserPlan).filter_by(id=userplan.id).first()
                    discounted_price = auctionplan.discount

                elif order.discount_status == OrderDiscountStatus.AUCTIONWINNER:
                    auction = current_user.auctions.join(Item).filter_by(id = order.item.id).order_by('auctions.created_at DESC').first()
                    offer = Offer.query.filter_by(auction_id=auction.id,win=True).first()
                    discounted_price = order.item.price - offer.total_price

                orders.append({
                "id" : order.id,
                "item_id" : order.item.id,
                "title" : title,
                "item_title" : item_title,
                "items_discount" : str(order.item.discount),
                "product_title" : product_title,
                "fulltitle" : product_title + " - " + item_title,
                "images" : order.item.images,
                "main_price" : str(order.total * order.item.price),
                "discounted_price" : str(order.total * order.item.price - discounted_price),
                "quantity" : order.item.quantity,
                "total" : order.total,
                "status" : order.status,
                "discount_status" : order.discount_status,
                })
            return make_response(jsonify(orders), 200)

class UserCoupons(Resource):
    @jwt_refresh_token_required
    def get(self):
        data = []
        for gift in current_user.gifts:
            if gift.title != COUPONCODE:
                user_gift = db.session.query(user_gifts).filter_by(user_id=current_user.id, gift_id=gift.id,used=False).first()
                if user_gift:
                    data.append({"code":gift.id,"title":gift.title ,"amount":str(gift.amount)})
                    # update extra field for relationship
                    # stmt = user_gifts.update().where(user_gifts.c.user_id==current_user.id,user_gifts.c.gift_id==gift.id).values(used=False)
                    # db.engine.execute(stmt)

        return make_response(jsonify(data), 200)

    @jwt_required
    def post(self):

        if(not current_user.is_authenticated):
            msg = "کوپن تخفیف فقط برای کاربران عضو تعریف شده است"
            return make_response(jsonify({"reason":msg, "success":False}),400)

        data = request.get_json(force=True)
        coupon_code = data.get("coupon", None)
        #handle invitor copun code
        if(coupon_code):
            coupon = Gift.query.filter_by(title = coupon_code).first()
            if(not coupon or coupon_code == COUPONCODE):
                msg ="کد تخفیف شما معتبر نمی باشد"
                return make_response(jsonify({"reason":msg}),400)
            if coupon.expired:
                msg =  "کوپن تخفیف مورد نظر منقضی شده است"
                return make_response(jsonify({"reason":msg}),400)

            gift_user = db.session.query(user_gifts).filter_by(user_id=current_user.id, gift_id=coupon.id).first()
            if gift_user:
                if gift_user.used:
                    msg = "کد تخفیف قبلا توسط شما استفاده شده است"
                    return make_response(jsonify({"reason":msg}),400)
                else:
                    msg = "این کوپن تخفیف قبلا برای سبد خرید شما ثبت شده است"
                    return make_response(jsonify({"code":coupon.id, "title":coupon.title, "amount":str(coupon.amount), "reason":msg,"success":False}),200)
            else:
                current_user.gifts.append(coupon)
                db.session.add(current_user)
                db.session.commit()
                msg ="کد تخفیف مورد نظر شما با موفقیت اعمال شد"
                return make_response(jsonify({"code":coupon.id, "title":coupon.title, "amount":str(coupon.amount), "reason":msg,"success":True}),200)

        msg ="لطفا کد تخفیف خود را وارد کنید"
        return make_response(jsonify({"reason":msg}),400)

    @jwt_required
    def delete(self):
        data = request.get_json(force=True)
        coupon_code = data.get("coupon_code", None)
        if coupon_code:
            db_coupon = Gift.query.get(coupon_code)
            user = db_coupon.users.filter_by(id=current_user.id).first()
            db_coupon.users.remove(user)
            db.session.add(db_coupon)
            db.session.commit()
            return make_response(jsonify({"msg":"کوپن خرید شما با موفقیت حذف شد"}), 200)

class UserCheckOutInit(Resource):
    def post(self):
        if (not current_user.is_authenticated):
            if "orders" in session:
                unpaid_orders = session['orders']
                payment = unpaid_orders[0][0]['payment']
                if not payment:
                    payment = Payment()
                else:
                    payment = Payment.query.get(payment[0]['id'])

                payment.type = PaymentType.PRODUCT
                payment.amount = 0
                payment.discount = 0
                payment.status = PaymentStatus.PAYING
                payment.details = str(unpaid_orders[0][0]['id'])

                payment.payment_method = PaymentMethod.query.filter_by(type=Payment_Types.Online).first()
                paymentschema = PaymentSchema()

                for order in unpaid_orders:
                    order[0]['status'] = OrderStatus.PAYING
                    payment.amount += float(order[0]['total_cost'])
                    payment.discount += float(order[0]['total_discount'])

                db.session.add(payment)
                db.session.commit()
                session['orders'][0][0]['payment'] = paymentschema.dump(payment)
        else:
            # unpaid_orders = Order.query.filter_by(user_id=current_user.id, status=OrderStatus.UNPAID).all()

            unpaid_orders = Order.query.filter_by(user_id=current_user.id).filter(or_(Order.status==OrderStatus.UNPAID,Order.status==OrderStatus.PAYING)).all()

            if not unpaid_orders:
                msg = "امکان پرداخت سبد خرید شما وجود ندارد لطفا پس از بررسی مجددا اقدام فرمایید"
                return make_response(jsonify({"success":False,"message":msg}),400)

            payment = Order.query.filter_by(user_id=current_user.id).filter(or_(Order.status==OrderStatus.UNPAID,Order.status==OrderStatus.PAYING)).first().payment
            if(not payment):
                payment = Payment()

            payment.type = PaymentType.PRODUCT
            payment.amount = 0
            payment.discount = 0

            payment.payment_method = PaymentMethod.query.filter_by(type=Payment_Types.Online).first()
            payment.status = PaymentStatus.PAYING

            gift_discount = 0
            user_gift = db.session.query(user_gifts).filter_by(user_id=current_user.id,used=False).all()
            for g in user_gift:
                gift = Gift.query.get(g.gift_id)
                if not gift.expired:
                    gift_discount += gift.amount
                    # stmt = user_gifts.update().where(and_(user_gifts.c.user_id==current_user.id,user_gifts.c.gift_id==gift.id)).values(used=True)
                    # db.engine.execute(stmt)
                else:
                    stmt = user_gifts.delete().where(and_(user_gifts.c.user_id==current_user.id,user_gifts.c.gift_id==gift.id))
                    db.engine.execute(stmt)

            for order in unpaid_orders:
                payment.amount += order.total_cost
                payment.discount += order.total_discount
                order.status = OrderStatus.PAYING

                if (not order.payment):
                    db.session.add(payment)
                    current_user.payments.append(payment)
                    db.session.add(current_user)

                order.payment = payment
                order.payment_id = payment.id

                db.session.add(order)
            payment.amount -= gift_discount
            payment.discount += gift_discount
            db.session.add(payment)
            db.session.commit()

            msg = "نمایش پیش فاکتور برای سفارش شما"
            return make_response(jsonify({'success':True,"type":"redirect_to_invoice","pid":payment.id,"message":msg}),200)

#TODO: *strict validation*
class UserCheckoutConfirm(Resource):
    @jwt_required
    def post(self, pid):
        data = parse_payment_account.parse_args()
        shipment_method = data['shipment_method']
        payment_method = data['payment_method']
        payment = Payment.query.get(pid)
        shipment_method = ShipmentMethod.query.get(shipment_method)
        payment_method = PaymentMethod.query.get(payment_method)

        if current_user.is_authenticated:

            if ('accept_tick' in data and data['accept_tick'] == "True"):
                current_user.first_name = data['first_name']
                current_user.last_name = data['last_name']
                # current_user.mobile = data['mobile']
                if current_user.mobile!=str(data['mobile']):
                    msg = "تغییر شماره همراه فقط از بخش پروفایل کاربری ممکن است"
                    return make_response(jsonify({"message":{"message":msg,"success":False}}),400)

                if 'work_place' in data:
                    current_user.work_place = data['work_place']
                if 'email' in data:
                    current_user.email = data['email']

                if(not current_user.address):
                    address = Address()
                    address.city = data['city']
                    address.address = data['address']
                    state = State.query.get(data['state'])
                    address.state = state
                    address.postal_code = data['postal_code']
                    try:
                        db.session.add(address)
                        db.session.commit()
                        current_user.address = address
                    except Exception as e:
                        return make_response(jsonify({"message":{"message": e.message}}), 500)
                else:
                    current_user.address.city = data['city']
                    current_user.address.address = data['address']
                    state = State.query.get(data['state'])
                    current_user.address.state = state
                    current_user.address.postal_code = data['postal_code']

                db.session.add(current_user)
                db.session.commit()

            if not payment:
                msg = "پرداخت معتبری برای سبد خرید شما موجود نیست.لطفا سبد خود را دوباره تشکیل دهید"
                return make_response(jsonify({"message":{"message":msg,"success":False}}),400)

            if payment.user_id != current_user.id:
                msg = "این عملیات پرداخت غیر مجاز است"
                return make_response(jsonify({"message":{"message":msg,"success":False}}),400)

            if payment.status == PaymentStatus.PAID:
                msg = "این صورتحساب قبلا پرداخت شده است"
                return make_response(jsonify({"message":{"message":msg,"operation":"redirect_to_profile","success":False}}),400)

            if payment.status == PaymentStatus.ARCHIVE:
                msg = "صورتحساب شما در بایگانی موجود است و امکان پرداخت آن نمی باشد"
                return make_response(jsonify({"message":{"message":msg,"operation":"redirect_to_profile","success":False}}),400)

            if payment_method.type == Payment_Types.Credit:
                if current_user.credit < payment.amount + shipment_method.price:
                    msg = "موجودی حساب شما برای پرداخت این صورتحساب کافی نیست"
                    return make_response(jsonify({"message" : {"message":msg,"operation":"redirect_to_profile","success":False}}),400)
                else:
                    current_user.credit -= payment.amount + shipment_method.price
                    db.session.add(current_user)
                    db.session.commit()

                    orders = Order.query.filter_by(payment_id=pid,user_id=current_user.id).all()

                    for order in orders:
                        shipment = Shipment.query.filter_by(order_id=order.id).first()
                        if shipment :
                            shipment.shipment_method = shipment_method
                            shipment.shipment_method_id = shipment_method.id
                            shipment.status = ShipmentStatus.READY_TO_SEND
                        else:
                            shipment = Shipment()
                            shipment.order_id = order.id
                            shipment.payment_id = pid
                            shipment.status = ShipmentStatus.READY_TO_SEND
                            shipment.shipment_method = shipment_method
                            shipment.shipment_method_id = shipment_method.id
                            order.shipment = shipment
                            if ('more_info' in data):
                                order.description = data['more_info']
                            db.session.add(shipment)
                        order.status = OrderStatus.PAID
                        db.session.add(order)
                        db.session.commit()

                    payment.amount += shipment_method.price
                    payment.status = PaymentStatus.ARCHIVE
                    payment.ref_id = random.randint(100000,10000000)
                    payment.sale_order_id = random.randint(1000000,1000000000)
                    payment.sale_refrence_id = random.randint(1000,1000000)
                    payment.GUID = random.randint(1000000000,100000000000)
                    payment.payment_method = payment_method
                    payment.payment_method_id = payment_method.id

                    user_gift = db.session.query(user_gifts).filter_by(user_id=current_user.id,used=False).all()
                    for g in user_gift:
                        gift = Gift.query.get(g.gift_id)
                        if gift:
                            stmt = user_gifts.update().where(and_(user_gifts.c.user_id==current_user.id,user_gifts.c.gift_id==gift.id)).values(used=True)
                            db.engine.execute(stmt)

                    db.session.add(payment)
                    db.session.commit()
                    msg = "مبلغ مورد نظر از حساب شما کسر شد و خرید با موفقیت انجام گرفت"
                    return make_response(jsonify({"message":{'success':True,"message":msg,"operation":"redirect_to_profile"}}),200)

            if payment_method.type == Payment_Types.Online:

                orders = Order.query.filter_by(payment_id=pid,user_id=current_user.id).all()

                for order in orders:
                    shipment = Shipment.query.filter_by(order_id=order.id).first()
                    if shipment :
                        shipment.shipment_method = shipment_method
                        shipment.shipment_method_id = shipment_method.id
                        # shipment.status = ShipmentStatus.IN_STORE
                    else:
                        shipment = Shipment()
                        shipment.order_id = order.id
                        shipment.payment_id = pid
                        # shipment.status = ShipmentStatus.IN_STORE
                        shipment.shipment_method = shipment_method
                        shipment.shipment_method_id = shipment_method.id

                    db.session.add(shipment)
                    db.session.commit()
                    order.shipment = shipment
                    order.status = OrderStatus.PAYING
                    db.session.add(order)
                    db.session.commit()

                payment.amount += shipment_method.price
                payment.payment_method = payment_method
                payment.payment_method_id = payment_method.id
                payment.sale_order_id = random.randint(1000000,1000000000)
                payment.sale_refrence_id = random.randint(1000,1000000)
                payment.GUID = random.randint(1000000000,100000000000)

                db.session.add(payment)
                db.session.commit()

                msg = "سبد خرید شما آماده پرداخت است . پیگیری های آتی خرید خود را از پروفایل کاربری خود انجام دهید"
                return make_response(jsonify({'message':{'success':True,"operation":"redirect_to_bank","pid":payment.id,"message":msg}}),200)
            else:
                msg = "روش پرداخت مورد نظر وجود ندارد"
                return make_response(jsonify({"message":{"message":{"message":msg,"success":False}}}),400)
        else:
            msg = "برای پرداخت صورتحساب باید به سایت وارد شوید"
            return make_response(jsonify({"message":{"message":msg,"success":False}}),400)

class UserApplyPayment(Resource):
    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        pid = data.get("pid", None)

        payment = Payment.query.get(pid)

        if(payment.user_id != current_user.id):
            return make_response(jsonify({"message":"انجام عملیات پرداخت برای شما مجاز نمیباشد"}),400)

        unpaid_user_plan = UserPlan.query.filter_by(payment_id=payment.id, user_id = current_user.id).first()

        if(payment.status == PaymentStatus.PAID):

            payment.status = PaymentStatus.ARCHIVE
            db.session.add(payment)
            db.session.commit()

            orders = Order.query.filter_by(payment_id=pid).all()

            if(unpaid_user_plan):
                if(not current_user.has_auction(unpaid_user_plan.auction)):
                    current_user.auctions.append(unpaid_user_plan.auction)
                    db.session.add(current_user)
                    db.session.commit()

                    auction = unpaid_user_plan.auction

                    already_invited = current_user.gifts.filter_by(title=COUPONCODE).first()
                    if not already_invited and current_user.invitor and (User.query.filter_by(invitor=current_user.invitor).count() < MAX_INVITOR_POLICY):
                        gift = Gift.query.filter_by(title=COUPONCODE).first()
                        if gift and not gift.expired:

                            g_payment = Payment()
                            g_payment.amount = gift.amount
                            g_payment.discount = 0
                            g_payment.status = PaymentStatus.PAID
                            g_payment.type = PaymentType.INVITOR_GIFT
                            g_payment.payment_method = PaymentMethod.query.filter_by(title='بدون پرداخت').first()
                            g_payment.user = current_user
                            db.session.add(g_payment)
                            db.session.commit()

                            current_user.gifts.append(gift)
                            current_user.credit += gift.amount
                            db.session.add(current_user)
                            db.session.commit()

                            title = str(auction.title).replace('حراجی','')
                            message = str(current_user) + ' عزیز ٬'
                            + '\n' + 'با شرکت شما در حراجی هدیه معرفی یونی بید برای شما اعمال شد.'\
                            + '\n' + 'www.unibid.ir'

                            auction_notification = SiteNotification()
                            auction_notification.title = 'دریافت هدیه دعوت از دوستان'
                            auction_notification.text = 'جهت هدیه معرفی دوستان به یونی بید٬ کیف پول شما به میزان' + str(int(gift.amount)) + ' تومان شارژ شد.'
                            auction_notification.sms = message
                            auction_notification.link = SITE_PREFIX+'/profile'
                            auction_notification.details = str(current_user)+";"+title+";"+str(int(gift.amount))
                            auction_notification.type = SiteNotificationType.INVITORGIFT
                            auction_notification.user = current_user
                            db.session.add(auction_notification)
                            db.session.commit()

                            invitor = User.query.filter_by(username=current_user.invitor).first()
                            if invitor:
                                g_payment = Payment()
                                g_payment.amount = gift.amount
                                g_payment.discount = 0
                                g_payment.status = PaymentStatus.ARCHIVE
                                g_payment.type = PaymentType.INVITOR_GIFT
                                g_payment.payment_method = PaymentMethod.query.filter_by(title='بدون پرداخت').first()
                                g_payment.user = invitor
                                db.session.add(g_payment)
                                db.session.commit()

                                invitor.credit += gift.amount
                                db.session.add(invitor)
                                db.session.commit()

                                remained_invitation_coupons = MAX_INVITOR_POLICY - User.query.filter_by(invitor=invitor.username).count()
                                title = str(auction.title).replace('حراجی','')
                                message = str(invitor) + ' عزیز ٬'\
                                + '\n' + 'با شرکت کردن دوست شما '+ str(current_user) +' در حراجی هدیه معرفی یونی بید برای شما فعال شد.'\
                                + '\n' + 'www.unibid.ir'

                                auction_notification = SiteNotification()
                                auction_notification.title = 'دریافت هدیه دعوت از دوستان'
                                auction_notification.text = 'جهت هدیه معرفی دوستان به یونی بید٬ کیف پول شما به میزان ' + str(int(gift.amount)) + ' تومان شارژ شد.'\
                                + '\n' + ' با دعوت از '+str(remained_invitation_coupons)+' نفر دیگر از دوستان خود می توانید شارژ هدیه معرفی را دریافت کنید.'
                                auction_notification.sms = message
                                auction_notification.link = SITE_PREFIX+'/profile'
                                auction_notification.details = str(invitor)+";"+str(current_user)+";"+title+";"+str(int(gift.amount))+";"+str(remained_invitation_coupons)
                                auction_notification.type = SiteNotificationType.INVITORSELFGIFT
                                auction_notification.user = invitor
                                db.session.add(auction_notification)
                                db.session.commit()


                    title = str(auction.title).replace('حراجی','')
                    message = current_user.username + ' عزیز ٬' \
                    + '\n' + 'مجوز شرکت در حراجی ' + title + ' برای شما صادر گردید.'\
                    + '\n' + SITE_PREFIX+'/auction/'+str(auction.id)\
                    + '\n' + 'با آرزوی موفقیت شما در حراجی'\
                    + '\n' + 'یونی بید'\
                    + '\n' + 'www.unibid.ir'

                    auction_notification = SiteNotification()
                    auction_notification.title = 'مجوز شرکت در حراجی'
                    auction_notification.text = 'مجوز شرکت در حراجی ' + title + 'برای شما صادر گردید'
                    auction_notification.sms = message
                    auction_notification.link = SITE_PREFIX+'/auction/'+str(auction.id)
                    auction_notification.details = current_user.username+";"+title+";"+SITE_PREFIX+'/auction/'+str(auction.id)
                    auction_notification.type = SiteNotificationType.PARTICIPATE
                    auction_notification.user = current_user
                    db.session.add(auction_notification)
                    db.session.commit()

            elif(orders):
                for order in orders:
                    shipment = Shipment.query.filter_by(order_id=order.id).first()
                    shipment.status = ShipmentStatus.READY_TO_SEND
                    order.status = OrderStatus.PAID

                    user_gift = db.session.query(user_gifts).filter_by(user_id=current_user.id,used=False).all()
                    for g in user_gift:
                        gift = Gift.query.get(g.gift_id)
                        if gift:
                            stmt = user_gifts.update().where(and_(user_gifts.c.user_id==current_user.id,user_gifts.c.gift_id==gift.id)).values(used=True)
                            db.engine.execute(stmt)

                    db.session.add(order)
                    db.session.add(shipment)
                    db.session.commit()
            else:
                current_user.credit += payment.amount
                db.session.add(current_user)
                db.session.commit()
            msg = "پرداخت موفق"
            return make_response(jsonify({"success":True,"message":msg,"token":payment.ref_id}),200)

        elif(payment.status== PaymentStatus.ARCHIVE):
            msg = "پرداخت بایگانی شده"
            return make_response(jsonify({"success":True,"message":msg,"token":payment.ref_id}),200)

        else:
            if unpaid_user_plan:
                UserPlan.query.filter_by(payment_id=payment.id, user_id = current_user.id).delete()
                db.session.commit()

            msg = "پرداخت ناموفق"
            return make_response(jsonify({"success":False,"message":msg,"token":payment.ref_id}),200)

class UserUnpaidOrders(Resource):
    @jwt_required
    def get(self):
        unpaid_orders = Order.query.filter_by(status=OrderStatus.UNPAID, user_id = current_user.id).all()
        order_schema = OrderSchema(many=True)
        return make_response(jsonify(order_schema.dump(unpaid_orders)), 200)

class UserUnpaidPayments(Resource):
    @jwt_required
    def get(self):
        unpaid_payments = Payment.query.filter_by(user_id=current_user.id, status=PaymentStatus.UNPAID).all()
        payment_schema = PaymentSchema(many=True)
        return make_response(jsonify(payment_schema.dump(unpaid_payments)), 200)

class UserAuctionLikes(Resource):
    def get(self):
        if(current_user.is_authenticated):
            return make_response(jsonify(AuctionSchema(many=True).dump(current_user.auction_likes)),200)
        else:
            return make_response(jsonify({"success":False,"message":"برای مشاهده علاقمندی ها باید لاگین کنید"}),400)

    @jwt_required
    def post(self):
        if current_user.is_authenticated:
            data = request.get_json(force=True)
            auction_id = data['auction_id']
            auction = Auction.query.get(auction_id)
            if(not auction in current_user.auction_likes):
                auction.likes.append(current_user)
                db.session.add(auction)
                db.session.commit()
                return make_response(jsonify({"success":"true","message":"حراجی به علاقمندی های شما اضافه شد"}),200)
            else:
                auction.likes.remove(current_user)
                db.session.add(auction)
                db.session.commit()
                return make_response(jsonify({"success":"true","message":"حراجی از علاقمندی های شما حذف شد"}),200)

        else:
            return make_response(jsonify({"message":"برای لایک کردن باید به سایت وارد شوید"}),400)

    #TODO: create new Route for this
    @jwt_required
    def delete(self):
        if current_user.is_authenticated:
            data = request.get_json(force=True)
            auction_id = data['auction_id']
            auction = Auction.query.get(auction_id)
            auction.likes.remove(current_user)
            db.session.add(auction)
            db.session.commit()
            return make_response(jsonify({"success":"true","message":"حراجی از علاقمندی های شما حذف شد"}),200)
        else:
            return make_response(jsonify({"message":"برای حذف لایک باید به سایت وارد شوید"}),400)

class UserFavoriteFilters(Resource):
    def get(self,order_by_price,order_by,total):
        now = datetime.now()
        result = None
        if order_by_price=="price":
            result = current_user.auction_likes.join(Item).order_by("price "+order_by).limit(total)
        else:
            result = current_user.auction_likes.order_by("start_date "+order_by).limit(total)

        auctions=[]
        for auction in result:
            auction_participants = []
            for participant in auction.participants:
                auction_participants.append({"id":participant.id,"username":participant.username})

            remained_time = (auction.start_date - now).days * 24 * 60 * 60 + (auction.start_date - now).seconds
            left_from_created = (now.replace(hour=0,minute=0,second=0,microsecond=0) - now).seconds
            liked = None
            if current_user.is_authenticated:
                liked = auction in current_user.auction_likes

            auctions.append({
            "id":auction.id,
            "item_id":auction.item.id,
            "title":auction.title,
            "images":auction.item.images,
            "base_price":str(auction.base_price),
            "max_price":str(auction.max_price),
            "main_price":str(auction.item.price),
            "remained_time":remained_time,
            "left_from_created":left_from_created,
            "liked":liked,
            "participants":auction_participants,
            "max_members":auction.max_members,
            })

        return make_response(jsonify(auctions),200)

class UserAuctionView(Resource):

    def get(self):
        if current_user.is_authenticated:
            auction_views = db.session.query(user_auction_views).filter_by(user_id = current_user.id).all()
            auctions = [Auction.query.get(auction_view.id) for auction_view in auction_views]
            auction_schema = AuctionSchema(many=True)
            return make_response(jsonify({"seen_auctions": auction_schema.dump(auctions)}), 200)
        else:
            return make_response(jsonify([]), 200)

    @jwt_required
    def post(self):
        if current_user.is_authenticated:
            data = request.get_json(force=True)
            auction_id = data.get('aid')
            auction = Auction.query.get(auction_id)
            if not db.session.query(user_auction_views).filter_by(user_id=current_user.id, auction_id=auction_id).scalar():
                current_user.auction_views.append(auction)
                db.session.add(current_user)
                db.session.commit()
                return make_response(jsonify({"success": True, "message": {"success": "حراجی به لیست مشاهده شده افزوده شد"}}), 200)
            return make_response(jsonify({"success": False, "message": {"failure": "این جراجی قبلا به لیست مشاهده شده افزوده شده است"}}), 200)
        return make_response(jsonify({"success":False,"message":"کاربر لاگین نکرده است"}),200)

class UserChargeWalet(Resource):
    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        charge_amount = data.get("charge_amount", None)

        payment_method = PaymentMethod.query.filter_by(type = Payment_Types.Online).first()

        payment = Payment()

        payment.type = PaymentType.WALET
        payment.amount = charge_amount
        payment.payment_method = payment_method
        payment.status = PaymentStatus.UNPAID
        payment.discount = 0

        current_user.payments.append(payment)
        db.session.add(current_user)
        db.session.commit()

        msg = " برای پرداخت به صفحه تایید هدایت می شوید"
        return make_response(jsonify({'success':True,"type":"redirect_to_bank","pid":payment.id,"text":msg}),200)

    @jwt_required
    def delete(self):
        data = request.get_json(force=True)
        pid = int(data.get("pid", None))
        Payment.query.filter_by(id=pid).delete()
        db.session.commit();
        msg = "پرداخت مورد نظر شما کنسل شد"
        return make_response(jsonify({'success':True,"operation":"cancel_payment","message":msg}),200)

class UserNotifications(Resource):
    # @jwt_required
    def get(self):
        result = []
        if (current_user.is_authenticated):
            notifs = SiteNotification.query.filter_by(user_id=current_user.id).order_by('created_at DESC').all()
            for notif in notifs:
                result.append({
                "id":notif.id,
                "title":notif.title,
                "text":notif.text,
                "seen":notif.seen,
                "link":notif.link,
                "date":str(notif.created_at),
                })

            notifs = UserNotification.query.filter_by(user_id=current_user.id).order_by('created_at DESC').all()
            for notif in notifs:
                result.append({
                "id":notif.notification.id,
                "title":notif.notification.title,
                "text":notif.notification.text,
                "seen":notif.seen,
                "link":notif.notification.link,
                "date":str(notif.notification.created_at),
                })

            notifs = UserAuctionNotification.query.filter_by(user_id=current_user.id).order_by('created_at DESC').all()
            for notif in notifs:
                result.append({
                "id":notif.auction_notification.id,
                "title":notif.auction_notification.title,
                "text":notif.auction_notification.text,
                "seen":notif.seen,
                "link":notif.auction_notification.link,
                "date":str(notif.auction_notification.created_at),
                })

            result = sorted(result, key=lambda r: r['date'],reverse=True)
        return make_response(jsonify(result),200)

    @jwt_required
    def post(self):
        result = []
        if(current_user.is_authenticated):
            data = request.get_json(force=True)
            nid = int(data.get("nid", None))
            user_notify = UserNotification.query.filter_by(user_id=current_user.id,notification_id=nid).first()
            auction_notify = UserAuctionNotification.query.filter_by(user_id=current_user.id,auction_notification_id=nid).first()
            site_notify = SiteNotification.query.filter_by(user_id=current_user.id,id=nid).first()
            if user_notify:
                user_notify.seen = True
                db.session.add(user_notify)
                db.session.commit()
            elif auction_notify:
                user_notify = UserAuctionNotification.query.filter_by(user_id=current_user.id,auction_notification_id=nid).first()
                if user_notify:
                    user_notify.seen = True
                    db.session.add(user_notify)
                    db.session.commit()
            elif site_notify:
                site_notify.seen = True
                site_notify.link = SITE_PREFIX
                db.session.add(site_notify)
                db.session.commit()

            notifs = SiteNotification.query.filter_by(user_id=current_user.id).order_by('created_at DESC').all()
            for notif in notifs:
                result.append({
                "id":notif.id,
                "title":notif.title,
                "text":notif.text,
                "seen":notif.seen,
                "link":notif.link,
                "date":str(notif.created_at),
                })

            notifs = UserNotification.query.filter_by(user_id=current_user.id).order_by('created_at DESC').all()
            for notif in notifs:
                result.append({
                "id":notif.notification.id,
                "title":notif.notification.title,
                "text":notif.notification.text,
                "seen":notif.seen,
                "link":notif.notification.link,
                "date":str(notif.notification.created_at),
                })

            notifs = UserAuctionNotification.query.filter_by(user_id=current_user.id).order_by('created_at DESC').all()
            for notif in notifs:
                result.append({
                "id":notif.auction_notification.id,
                "title":notif.auction_notification.title,
                "text":notif.auction_notification.text,
                "seen":notif.seen,
                "link":notif.auction_notification.link,
                "date":str(notif.auction_notification.created_at),
                })

            result = sorted(result, key=lambda r: r['date'],reverse=True)
        return make_response(jsonify(result),200)

    @jwt_required
    def put(self):
        if (current_user.is_authenticated):
            user_notify = UserNotification.query.filter_by(user_id=current_user.id).all()
            auction_notify = UserAuctionNotification.query.filter_by(user_id=current_user.id).all()
            site_notify = SiteNotification.query.filter_by(user_id=current_user.id).all()

            for notify in user_notify:
                notify.seen = True
                db.session.add(notify)
                db.session.commit()

            for notify in auction_notify:
                notify.seen = True
                db.session.add(notify)
                db.session.commit()

            for notify in site_notify:
                notify.seen = True
                db.session.add(notify)
                db.session.commit()

            return make_response(jsonify({"success":True,"message":"OK"}),200)
