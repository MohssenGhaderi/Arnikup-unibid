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

        chest = Chest.query.get(payload['chestId'])

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
            db.session.add(payment)
            db.session.add(user_chest)
            db.session.commit()
        else:
            user_chest.payment.status = PaymentStatus.RETRY
            db.session.add(user_chest)
            db.session.commit()



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
        pass

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
        pass

buy_avatar_fields = buy_ns.model('BuyAvatarModel', {
    "avatarId":fields.Integer()
})

@buy_ns.route('/avatar')
class BuyAvatar(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @buy_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @buy_ns.doc('buy avatar api.', parser=parser, body=buy_avatar_fields, validate=True)
    @buy_ns.response(200, 'Success')
    @token_required
    def post(self,current_user):
        pass
