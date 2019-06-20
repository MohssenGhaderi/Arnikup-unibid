from ..model import *
from flask_restplus import Resource, fields, Namespace
from flask import url_for, redirect, request, abort, make_response , jsonify , session, flash
from project import app, rest_api
from datetime import datetime
from sqlalchemy import or_, asc, desc
from ..model.guest_message import GuestMessage
from project.utils import token_required, token_optional
from project.helpers import *
from project.lang.fa import *
from definitions import SITE_PREFIX, COINS_BASE_PRICE, GEMS_BASE_PRICE
import math

buy_ns = Namespace('buy')

buy_chest_fields = buy_ns.model('BuyChestModel', {
    "chestId":fields.Integer()
})

@buy_ns.route('/chest')
class BuyChest(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @buy_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @buy_ns.doc('buy chest api.', parser=parser, body=buy_chest_fields, validate=True)
    @buy_ns.response(200, 'Success')
    @token_required
    def post(self,current_user):

        if 'chestId' not in buy_ns.payload:
            return make_response(jsonify({"success":False,"reason":"chestId","message":BUY_REQUIRED['chestId']}),400)

        chest = Chest.query.get(buy_ns.payload['chestId'])

        if not chest:
            return make_response(jsonify({"success":False,"reason":"chest","message":BUY_NOT_FOUND['chest']}),400)

        user_chest = UserChest.query.filter_by(chest_id=chest.id,user_id=current_user.id).first()
        if not user_chest:
            user_chest = UserChest()
            user_chest.user = current_user
            user_chest.chest = chest

            avatar_price = 0
            for avatar in chest.avatars:
                avatar_price += avatar.needed_gems * GEMS_BASE_PRICE
            chest_main_price = float(chest.coin.price) + float(chest.gem.price) + avatar_price
            chest_discount_price = chest_main_price - chest.discount * (float(chest.coin.price) + float(chest.gem.price) + avatar_price)

            payment = Payment()
            payment.amount = chest_discount_price
            payment.discount = chest_main_price - chest_discount_price
            payment.type = PaymentType.CHEST
            user_chest.payment = payment
            payment.user = current_user
            db.session.add(payment)
            db.session.add(user_chest)
            db.session.commit()
            return make_response(jsonify({"success":True,"message":BUY_CONFIRM ,'GUID':payment.GUID}),200)
        else:
            user_chest.payment.status = PaymentStatus.RETRY
            db.session.add(user_chest)
            db.session.commit()
            return make_response(jsonify({"success":True,"message":BUY_CONFIRM ,'GUID':user_chest.payment.GUID}),200)


buy_coin_fields = buy_ns.model('BuyCoinModel', {
    "coinId":fields.Integer()
})

@buy_ns.route('/coin')
class BuyCoin(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @buy_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @buy_ns.doc('buy coin api.', parser=parser, body=buy_coin_fields, validate=True)
    @buy_ns.response(200, 'Success')
    @token_required
    def post(self,current_user):

        if 'coinId' not in buy_ns.payload:
            return make_response(jsonify({"success":False,"reason":"coinId","message":BUY_REQUIRED['coinId']}),400)

        coin = Coin.query.get(buy_ns.payload['coinId'])

        if not coin:
            return make_response(jsonify({"success":False,"reason":"coinNotFound","message":BUY_NOT_FOUND['coin']}),400)

        payment = Payment()
        payment.amount = coin.price
        payment.type = PaymentType.COIN
        payment.status = PaymentStatus.UNPAID
        payment.discount = 0
        payment.user = current_user

        user_coin = UserCoin()
        user_coin.user = current_user
        user_coin.coin = coin
        user_coin.payment = payment

        db.session.add(payment)
        db.session.add(user_coin)
        db.session.commit()

        return make_response(jsonify({"success":True,"message":BUY_CONFIRM ,'GUID':payment.GUID}),200)


buy_gem_fields = buy_ns.model('BuyGemModel', {
    "gemId":fields.Integer()
})

@buy_ns.route('/gem')
class BuyGem(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @buy_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @buy_ns.doc('buy gem api.', parser=parser, body=buy_gem_fields, validate=True)
    @buy_ns.response(200, 'Success')
    @token_required
    def post(self,current_user):
        if 'gemId' not in buy_ns.payload:
            return make_response(jsonify({"success":False,"reason":"gemId","message":BUY_REQUIRED['gemId']}),400)

        gem = Gem.query.get(buy_ns.payload['gemId'])

        if not gem:
            return make_response(jsonify({"success":False,"reason":"gemNotFound","message":BUY_NOT_FOUND['gem']}),400)

        payment = Payment()
        payment.amount = gem.price
        payment.type = PaymentType.GEM
        payment.status = PaymentStatus.UNPAID
        payment.discount = 0
        payment.user = current_user

        user_gem = UserGem()
        user_gem.user = current_user
        user_gem.gem = gem
        user_gem.payment = payment

        db.session.add(payment)
        db.session.add(user_gem)
        db.session.commit()

        return make_response(jsonify({"success":True,"message":BUY_CONFIRM ,'GUID':payment.GUID}),200)


@buy_ns.route('/product')
class BuyProduct(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @buy_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @buy_ns.doc('buy product api.', parser=parser, validate=True)
    @buy_ns.response(200, 'Success')
    @token_required
    def post(self,current_user):
        unpaid_orders = Order.query.filter_by(user_id = current_user.id,status = OrderStatus.UNPAID).order_by(Order.created.desc())
        if not unpaid_orders:
            return make_response(jsonify({"success":False,"message":PAYMENT['NOORDERS']}),403)

        payment = unpaid_orders.first().payment
        if not payment:
            payment = Payment()
        payment.type = PaymentType.PRODUCT

        payment.amount = 0
        payment.discount = 0

        return make_response(jsonify({"success":True,"message":BUY_CONFIRM ,'GUID':1}),200)
