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


user_ns = Namespace('user')

@user_ns.route('/basic')
class Basic(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('get user basic information api.', parser=parser, validate=False)
    @user_ns.response(200, 'Success')
    @user_ns.response(400, 'SMS System and Validation Error')
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def get(self,current_user):
        result = []
        notifs = SiteNotification.query.filter_by(user_id=current_user.id).order_by(SiteNotification.created.desc())
        for notif in notifs:
            result.append({
            "id":notif.id,
            "title":notif.title,
            "text":notif.text,
            "seen":notif.seen,
            "link":notif.link,
            "date":str(notif.created),
            "image":notif.image,
            })

        notifs = UserNotification.query.filter_by(user_id=current_user.id).order_by(UserNotification.created.desc())
        for notif in notifs:
            result.append({
            "id":notif.notification.id,
            "title":notif.notification.title,
            "text":notif.notification.text,
            "seen":notif.seen,
            "link":notif.notification.link,
            "date":str(notif.notification.created),
            "image":'',
            })

        notifs = UserAuctionNotification.query.filter_by(user_id=current_user.id).order_by(UserAuctionNotification.created.desc())
        for notif in notifs:
            result.append({
            "id":notif.auction_notification.id,
            "title":notif.auction_notification.title,
            "text":notif.auction_notification.text,
            "seen":notif.seen,
            "link":notif.auction_notification.link,
            "date":str(notif.auction_notification.created),
            "image":notif.auction_notification.auction.image.split("'")[1],
            })

        result = sorted(result, key=lambda r: r['date'],reverse=True)

        basics = {
            "coins":current_user.coins,
            "gems":current_user.gems,
            "username":current_user.username,
            "avatar":current_user.avatar.image.split("'")[1],
            # "orderCount":Order.query.filter_by(user_id = current_user.id,status = OrderStatus.UNPAID).count(),
            "level":current_user.level.number,
            "notifications":result
        }
        return make_response(jsonify(basics),200)

@user_ns.route('/avatars')
class Avatars(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('get user avatars api.', parser=parser, validate=False)
    @user_ns.response(200, 'Success')
    @user_ns.response(400, 'SMS System and Validation Error')
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def get(self,current_user):

        avatar_result = Avatar.query.order_by(Avatar.created.desc(),Avatar.needed_gems.desc())
        avatars = []
        for avatar in avatar_result:
            free = True
            selected = False
            if avatar.needed_gems > 0:
                free = False
            if avatar.id == current_user.avatar.id:
                selected = True

            avatars.append({
                "image" : avatar.image.split("'")[1],
                "avatarId" : avatar.id,
                "title" : avatar.title,
                "free" : free,
                "selected" : selected,
                "gemsNeed" : avatar.needed_gems,
                "owned" : avatar in current_user.avatars
            })

        return make_response(jsonify(avatars),200)

    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('get user avatars api.', parser=parser, validate=False)
    @user_ns.response(200, 'Success')
    @user_ns.response(400, 'SMS System and Validation Error')
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def post(self,current_user):
        if 'avatarId' not in user_ns.payload:
            return make_response(jsonify({"success":False,"reason":"avatarId","message":AVATAR['REQUIRED']}),400)
        avatar = Avatar.query.get(user_ns.payload['avatarId'])

        if not avatar:
            return make_response(jsonify({"success":False,"reason":"avatarId","message":AVATAR['INVALID']}),400)

        if current_user.avatar.id == avatar.id:
            return make_response(jsonify({"success":False,"reason":"selectedAvatar","message":AVATAR['REAPETED']}),400)

        if avatar in current_user.avatars:
            current_user.avatar = avatar
            db.session.add(current_user)
            db.session.commit()
            return make_response(jsonify({"success":True,"message":USER['AVATAR_CHANGED']}),200)


        if current_user.gems < avatar.needed_gems:
            return make_response(jsonify({"success":False,"reason":"avatarGems","message":AVATAR['GEMS']}),400)

        gem_payment = GemPayment()
        gem_payment.paid_gems = avatar.needed_gems
        gem_payment.type = GemPayType.AVATAR
        gem_payment.status = GemPayStatus.DONE
        gem_payment.user = current_user

        user_avatar = UserAvatar()
        user_avatar.user = current_user
        user_avatar.gem_payment = gem_payment
        user_avatar.avatar = avatar

        user_agent_string = request.user_agent.string.encode('utf-8')
        user_agent_hash = hashlib.md5(user_agent_string).hexdigest()
        rj.jsonset(user_agent_hash, Path('.avatar'),avatar.image.split("'")[1])

        current_user.gems -= avatar.needed_gems
        current_user.avatar = avatar

        db.session.add(current_user)
        db.session.add(gem_payment)
        db.session.add(user_avatar)
        db.session.commit()
        return make_response(jsonify({"success":True,"message":USER['AVATAR_CHANGED_GEM']}),200)

@user_ns.route('/information')
class Information(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('get user basic information api.', parser=parser, validate=False)
    @user_ns.response(200, 'Success')
    @user_ns.response(400, 'SMS System and Validation Error')
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def get(self,current_user):
        user = {
            "username":current_user.username,
            "fullName":current_user.full_name,
            "mobile":current_user.mobile,
            "email":current_user.email,
            "level":current_user.level.number,
            "maxLevel":Level.query.count(),
            "avatar":current_user.avatar.image.split("'")[1],
            "orderCount":Order.query.filter_by(user_id = current_user.id,status = OrderStatus.UNPAID).count(),
        }
        return make_response(jsonify(user),200)

shipment_method_model = user_ns.model('ShipmentMethodModel', {
    "methodId":fields.Integer(),
    "title":fields.String(),
    "price":fields.String(),
})
item_garanty_model = user_ns.model('ItemGarantyModel', {
    "garantyId":fields.Integer(),
    "title":fields.String(),
    "price":fields.String(),
})

order_detail = user_ns.model('OrderDetailModel', {
    "orderId":fields.Integer(),
    "item_garanties":fields.List(fields.Nested(item_garanty_model)),
})

cart_fields_model = user_ns.model('ShoppingCartModel', {
    "count":fields.Integer(),
    "orderId":fields.Integer(),
    "itemId":fields.Integer(),
    "price":fields.Integer(),
    "type":fields.String(),
    "discount":fields.Integer(),
    "title":fields.String(),
    "image":fields.String(),
    "order_details" : fields.List(fields.Nested(order_detail))
})

shipment_methods_model = user_ns.model('ShipmentMethodsModel', {
    "shipment_methods" : fields.List(fields.Nested(shipment_method_model))
})


cart_put_fields = user_ns.model('ShoppingCartPut', {
    "orderId":fields.Integer()
})

cart_post_fields = user_ns.model('ShoppingCartPost', {
    "auctionId":fields.Integer()
})

@user_ns.route('/carts')
class cart(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('get user shopping cart information api.', parser=parser , validate=False)
    @user_ns.response(200, 'Success',cart_fields_model)
    @user_ns.response(400, 'SMS System and Validation Error')
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def get(self,current_user):
        order_result = Order.query.filter_by(user_id = current_user.id,status = OrderStatus.UNPAID).order_by(Order.created.desc())
        orders = []
        shipment_methods = []
        item_garanties = None
        Ids  = []
        for order in order_result:
            shipment_cost = 0
            for method in ItemShipment.query.join(ShipmentMethod).filter(ItemShipment.item_id==order.item_id).order_by(ShipmentMethod.title.desc()):
                if method.shipment_method.id not in Ids:
                    shipment_methods.append({
                        "methodId":method.shipment_method.id,
                        "title":method.shipment_method.title,
                        "price": method.shipment_method.aggrigation * float(method.price)
                    })
                    Ids.append(method.shipment_method.id)
                else:
                    item = next(x for x in shipment_methods if x['methodId']==method.shipment_method.id)
                    item['price'] += method.shipment_method.aggrigation * float(method.price)

        for order in order_result:

            item_garanties = []
            for item_garanty in ItemGaranty.query.join(Garanty).filter(ItemGaranty.item_id==order.item_id).order_by(ItemGaranty.price):
                item_garanties.append({
                    "orderId":order.id,
                    "garantyId":item_garanty.garanty.id,
                    "title":item_garanty.garanty.title,
                    "price":int(item_garanty.price)
                })

            orders.append({
                "orderId":order.id,
                "itemId":order.item.id,
                "price":str(order.total_cost),
                "discount":str(order.total_discount),
                "title":order.item.title,
                "type":order.discount_status,
                "image":order.item.images.split("'")[1],
                "order_details":{
                    "item_garanties":item_garanties
                }
            })

        print(shipment_methods)
        return make_response(jsonify(orders),200)

    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('delet user shopping cart item api.', parser=parser, body=cart_put_fields, validate=False)
    @user_ns.response(200, 'delete item from shopping cart')
    @user_ns.response(400, 'SMS System and Validation Error')
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def put(self,current_user):
        if 'orderId' not in user_ns.payload:
            return make_response(jsonify({"success":False,"reason":"orderId","message":ORDER['REQUIRED']}),400)
        orderId = user_ns.payload['orderId']
        order = Order.query.get(orderId)
        if not order:
            return make_response(jsonify({"success":False,"reason":"orderId","message":ORDER['INVALID']}),403)

        Order.query.filter_by(id=orderId).delete()
        db.session.commit()
        return make_response(jsonify({"success":True,"message":ORDER['DELETE_SUCCESS']}),200)

    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('get user shopping cart information api.', parser=parser,body=cart_post_fields, validate=False)
    @user_ns.response(200, 'add item to shopping cart')
    @user_ns.response(400, 'SMS System and Validation Error')
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def post(self,current_user):
        if 'auctionId' not in user_ns.payload:
            return make_response(jsonify({"success":False,"auctionId":"orderId","message":AUCTION['REQUIRED']}),400)

        auction = Auction.query.get(user_ns.payload['auctionId'])
        if not auction:
            return make_response(jsonify({"success":False,"reason":"auctionId","message":AUCTION['NOT_FOUND']}),403)
        item = Item.query.get(auction.item.id)
        if not item:
            return make_response(jsonify({"success":False,"reason":"itemId","message":ITEM['INVALID']}),403)

        last_order = Order.query.filter_by(user_id=current_user.id,item_id=item.id, status=OrderStatus.UNPAID).first()
        if(last_order):
            return make_response(jsonify({"success":False,"reason":"orderRepeated","message":ORDER['REAPETED']}),403)

        if item.quantity ==0:
            return make_response(jsonify({"success":False,"reason":"itemQuantity","message":ITEM['QUANTITY']}),403)


        item_price = item.price - item.discount
        discount_status = OrderDiscountStatus.REGULAR
        discount = item.discount

        last_bid = Bid.query.filter_by(auction_id=auction.id).order_by(Bid.created.desc()).first()
        if last_bid:
            if last_bid.user_plan.user.id==current_user.id and last_bid.won:
                # item_price = last_bid.total_price
                discount_status = OrderDiscountStatus.AUCTIONWINNER
                discount = item.price - last_bid.total_price
            else:
                user_plan = UserPlan.query.join(AuctionPlan).filter(AuctionPlan.auction_id==auction.id,UserPlan.user_id==current_user.id).first()
                discount = user_plan.auction_plan.discount
                # item_price = item.price - user_plan.auction_plan.discount
                discount_status = OrderDiscountStatus.INAUCTION
        else:
            if auction in current_user.auctions:
                user_plan = UserPlan.query.join(AuctionPlan).filter(AuctionPlan.auction_id==auction.id,UserPlan.user_id==current_user.id).first()
                discount = user_plan.auction_plan.discount
                # item_price = item.price - user_plan.auction_plan.discount
                discount_status = OrderDiscountStatus.INAUCTION

        order = Order()
        order.item = item
        order.user = current_user
        order.total = 1
        order.total_cost = item_price
        order.total_discount = discount
        order.discount_status = discount_status
        order.status = OrderStatus.UNPAID

        item.quantity -= 1
        db.session.add(item)
        db.session.add(order)
        db.session.commit()
        return make_response(jsonify({"success":True,"message":ORDER['ADD_SUCCESS']}),200)

@user_ns.route('/shipment/methods')
class ShipmentMedhods(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('get user shopping cart information api.', parser=parser , validate=False)
    @user_ns.response(200, 'Success',shipment_methods_model)
    @user_ns.response(400, 'SMS System and Validation Error')
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def get(self,current_user):
        order_result = Order.query.filter_by(user_id = current_user.id,status = OrderStatus.UNPAID).order_by(Order.created.desc())
        orders = []
        shipment_methods = []
        item_garanties = None
        Ids  = []
        for order in order_result:
            shipment_cost = 0
            for method in ItemShipment.query.join(ShipmentMethod).filter(ItemShipment.item_id==order.item_id).order_by(ShipmentMethod.title.desc()):
                if method.shipment_method.id not in Ids:
                    shipment_methods.append({
                        "methodId":method.shipment_method.id,
                        "title":method.shipment_method.title,
                        "price": method.shipment_method.aggrigation * float(method.price)
                    })
                    Ids.append(method.shipment_method.id)
                else:
                    item = next(x for x in shipment_methods if x['methodId']==method.shipment_method.id)
                    item['price'] += method.shipment_method.aggrigation * float(method.price)

        return make_response(jsonify(shipment_methods),200)

@user_ns.route('/scores')
class Scores(Resource):
    def get(self):
        oldUsers = User.query.order_by(User.points.desc()).limit(10)
        row = 0
        last_point = 999999999999999
        users = []
        for user in oldUsers:
            if last_point > user.points:
                row += 1
                last_point = user.points

            users.append({
                "row":row,
                "id":user.id,
                "points":user.points,
                "name":user.username,
                "level":user.level.number,
                "avatar":user.avatar.image.split("'")[1],
            })
        return make_response(jsonify(users),200)

@user_ns.route('/profile')
class Profile(Resource):
    @token_required
    def get(self,current_user):
        states = []
        for state in State.query.order_by(State.title.asc()).distinct().all():
            states.append({
            "id":state.id,
            "title":state.title
            })
        state = None
        city = None
        address = None
        if current_user.address:
            state = current_user.address.state.title
            city = current_user.address.city
            address = current_user.address.address

        user = {
            "fullName":current_user.full_name,
            "email":current_user.email,
            "state":state,
            "city":city,
            "address":address,
            "avatar":current_user.avatar.image.split("'")[1],
            "states":states,
        }
        return make_response(jsonify(user),200)

    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('get user shopping cart information api.', parser=parser, validate=False)
    @user_ns.response(200, 'Success')
    @user_ns.response(400, 'SMS System and Validation Error')
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def post(self,current_user):
        if(not current_user.address):
            address = Address()
            address.city = user_ns.payload['city']
            address.address = user_ns.payload['address']
            address.state = State.query.get(user_ns.payload['state'])
            db.session.add(address)
            db.session.commit()
            current_user.address = address
        else:
            current_user.address.city = user_ns.payload['city']
            current_user.address.address = user_ns.payload['address']
            current_user.address.state = State.query.get(user_ns.payload['state'])

        current_user.full_name = user_ns.payload['fullName']
        current_user.email = user_ns.payload['email']
        db.session.add(current_user)
        db.session.commit()

        return make_response(jsonify({"success":True,"message":USER['PROFILE_SAVED']}),200)

@user_ns.route('/address')
class GetAddress(Resource):
    @token_required
    def get(self,current_user):
        state = None
        city = None
        address = None
        if current_user.address:
            state = current_user.address.state.title
            city = current_user.address.city
            address = current_user.address.address

        address = {
            "state":state,
            "city":city,
            "address":address,
            "fullName":current_user.full_name,
            "workPlace":current_user.work_place
        }
        return make_response(jsonify(address),200)

@user_ns.route('/shipment')
class ShipmentInfo(Resource):
    @token_required
    def get(self,current_user):

        states = []
        for state in State.query.order_by(State.title.asc()).distinct().all():
            states.append({
            "id":state.id,
            "title":state.title
            })

        state = None
        city = None
        address = None
        if current_user.address:
            state = current_user.address.state.title
            city = current_user.address.city
            address = current_user.address.address

        result = {
            "fullName":current_user.full_name,
            "email":current_user.email,
            "state":state,
            "city":city,
            "address":address,
            "workPlace":current_user.work_place,
            "states":states,
        }

        return make_response(jsonify(result),200)

    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('get user shopping cart information api.', parser=parser, validate=False)
    @user_ns.response(200, 'Success')
    @user_ns.response(400, 'SMS System and Validation Error')
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def post(self,current_user):
        if(not current_user.address):
            address = Address()
            address.city = user_ns.payload['city']
            address.address = user_ns.payload['address']
            address.state = State.query.get(user_ns.payload['state'])
            db.session.add(address)
            db.session.commit()
            current_user.address = address
        else:
            current_user.address.city = user_ns.payload['city']
            current_user.address.address = user_ns.payload['address']
            current_user.address.state = State.query.get(user_ns.payload['state'])

        current_user.full_name = user_ns.payload['fullName']
        current_user.email = user_ns.payload['email']
        current_user.work_place = user_ns.payload['workPlace']
        db.session.add(current_user)
        db.session.commit()

        return make_response(jsonify({"success":True,"message":USER['PROFILE_SAVED']}),200)

paymentInfo_fields = user_ns.model('PaymentInfoModel', {
    "type":fields.String(),
    "title":fields.String(),
    "price":fields.Integer(),
    "paid":fields.Integer(),
    "factor":fields.String(),
    "date":fields.String(),
    "discount":fields.Integer(),
    "quantity":fields.Integer(),
    "image":fields.String(),
})

@user_ns.route('/payment')
class PaymentInfo(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('get user payment information api.', parser=parser , validate=False)
    @user_ns.response(200, 'Success',paymentInfo_fields)
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def get(self,current_user):
        result = Payment.query.filter_by(user_id=current_user.id,status=PaymentStatus.ARCHIVE).order_by(Payment.created.desc()).limit(5)
        payments = []
        for payment in result:
            if(payment.type==PaymentType.PRODUCT):
                order_result = Order.query.filter_by(payment_id=payment.id).all()
                for order in order_result:
                    payments.append({
                        "type":"p",
                        "title":" خرید محصول " + order.item.title ,
                        "price":str(order.item.price),
                        "paid":str(order.total_cost - order.total_discount),
                        "factor":payment.GUID,
                        "date":str(payment.updated),
                        "discount":str(order.total_discount),
                        "quantity":order.total,
                        "image":order.item.images.split("'")[1]
                    })

        return make_response(jsonify(payments),200)

coupons_field = user_ns.model('Coupons', {
    "couponCode":fields.List(fields.String)
})

user_coupon_field = user_ns.model('UserCoupon', {
    "title":fields.String(),
    "amount":fields.String(),
})

@user_ns.route('/coupons')
class Coupons(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('user coupon api.', parser=parser , validate=False)
    @user_ns.response(200, 'Success',)
    @user_ns.response(400, 'SMS System and Validation Error')
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def get(self,current_user):
        user_coupon = current_user.coupons.filter(UserCoupon.used==False).order_by(UserCoupon.created.desc()).first()
        result = None
        if user_coupon:
            result = {"title":user_coupon.title,"amount":str(user_coupon.amount)}

        return make_response(jsonify(result),200)

    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('user coupon api.', parser=parser , body=coupons_field, validate=False)
    @user_ns.response(200, 'Success')
    @user_ns.response(400, 'SMS System and Validation Error')
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def put(self,current_user):
        if 'couponCode' not in user_ns.payload:
            return make_response(jsonify({"success":False,"reason":"couponCode","message":COUPON['REQUIRED']}),400)

        coupon = Coupon.query.filter_by(title=user_ns.payload['couponCode']).first()

        if not coupon:
            return make_response(jsonify({"success":False,"reason":"couponNotFound","message":COUPON['INVALID']}),400)

        if coupon.expired:
            return make_response(jsonify({"success":False,"reason":"couponNotFound","message":COUPON['EXPIRED']}),403)


        user_coupon = UserCoupon.query.filter_by(user_id=current_user.id,coupon_id=coupon.id).first()
        if user_coupon:
            if user_coupon.used:
                return make_response(jsonify({"success":False,"reason":"couponUsed","message":COUPON['USED']}),403)

            message = COUPON['REAPETED'].replace('amount',str(int(coupon.amount)))
            return make_response(jsonify({"success":True,"reason":"couponReapeted","message":message}),200)

        if coupon.type == CouponType.SYSTEM:
            return make_response(jsonify({"success":False,"reason":"systemCoupon","message":COUPON['SYSTEM']}),403)

        current_user.coupons.append(coupon)
        db.session.add(current_user)
        db.session.commit()

        message = COUPON['STATUS'].replace('amount',str(int(coupon.amount)))
        return make_response(jsonify({"success":True,"message":message}),200)

    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @user_ns.doc('user coupon api.', parser=parser , body=coupons_field, validate=False)
    @user_ns.response(200, 'Success')
    @user_ns.response(400, 'SMS System and Validation Error')
    @user_ns.response(401, 'Not Authorized')
    @user_ns.response(403, 'Not available')
    @token_required
    def post(self,current_user):
        if 'couponCode' not in user_ns.payload:
            return make_response(jsonify({"success":False,"reason":"couponCode","message":COUPON['REQUIRED']}),400)

        coupon = Coupon.query.filter_by(title=user_ns.payload['couponCode']).first()

        if not coupon:
            return make_response(jsonify({"success":False,"reason":"couponNotFound","message":COUPON['INVALID']}),400)

        if coupon.expired:
            return make_response(jsonify({"success":False,"reason":"couponNotFound","message":COUPON['EXPIRED']}),403)

        user_coupon = UserCoupon.query.filter_by(user_id=current_user.id,coupon_id=coupon.id).first()
        if not user_coupon:
            return make_response(jsonify({"success":False,"reason":"couponNotFound","message":COUPON['NOT_YOURS']}),403)

        if user_coupon.used:
            return make_response(jsonify({"success":False,"reason":"couponUsed","message":COUPON['USED']}),403)

        unpaid_order = Order.query.filter_by(user_id=current_user.id,status=OrderStatus.UNPAID).first()
        unpaid_order.total_discount += coupon.amount
        user_coupon.used = True

        db.session.add(unpaid_order)
        db.session.add(user_coupon)
        db.session.commit()

        message = COUPON['FIXED'].replace('amount',str(int(coupon.amount)))
        return make_response(jsonify({"success":True,"message":message}),200)


# @user_ns.route('/order/details')
# class GetOrderDetails(Resource):
#     parser = rest_api.parser()
#     parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token',required=False)
#     @user_ns.header('Authorization: Bearer', 'JWT TOKEN', required=False)
#     @user_ns.doc(parser=parser,validate=True)
#     @user_ns.response(200, "Success",order_details_model)
#     @token_required
#     def get(self,current_user):
#         order_result = Order.query.filter_by(user_id = current_user.id,status = OrderStatus.UNPAID).order_by(Order.created.desc())
#         result = []
#         for order in order_result:
#
#             orderId = order.id
#
#             shipment_methods = []
#             for method in ItemShipment.query.join(ShipmentMethod).filter(ItemShipment.item_id==order.item_id).order_by(ShipmentMethod.title.desc()):
#                 shipment_methods.append({
#                     "methodId":method.shipment_method.id,
#                     "title":method.shipment_method.title,
#                     "price":str(method.price)
#                 })
#
#             item_garanties = []
#             for item_garanty in ItemGaranty.query.join(Garanty).filter(ItemGaranty.item_id==order.item_id).order_by(Garanty.title.desc()):
#                 item_garanties.append({
#                     "methodId":item_garanty.garanty.id,
#                     "title":item_garanty.garanty.title,
#                     "price":str(item_garanty.price)
#                 })
#
#             result.append({
#                 "order_details":{
#                     "orderId":orderId,
#                     "shipment_methods":shipment_methods,
#                     "item_garanties":item_garanties
#                 }
#             })
#         return make_response(jsonify(result),200)
