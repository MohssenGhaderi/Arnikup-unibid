from ..model import *
from flask_restplus import Resource, fields, Namespace
from flask import url_for, redirect, request, abort, make_response , jsonify , session, flash
from project import app, db, rest_api
from datetime import datetime
from sqlalchemy import or_, asc, desc
from ..model.guest_message import GuestMessage
from project.utils import token_required, token_optional
from project.helpers import *
from project.lang.fa import *
from definitions import SITE_PREFIX, COINS_BASE_PRICE, GEMS_BASE_PRICE
import math

shop_ns = Namespace('shop')

chest_base_model = shop_ns.model('ChestModel', {
    "chestId":fields.Integer(),
    "image":fields.String(),
    "title":fields.String(),
    "description":fields.String(),
    "discount":fields.Integer(),
    "discountedPrice":fields.Integer(),
})
coins_base_model = shop_ns.model('CoinModel', {
    "coinId":fields.Integer(),
    "title":fields.String(),
    "description":fields.String(),
    "price":fields.Integer(),
    "quantity":fields.Integer(),
    "discount":fields.Integer(),
})
gems_base_model = shop_ns.model('GemModel', {
    "gemId":fields.Integer(),
    "title":fields.String(),
    "description":fields.String(),
    "price":fields.Integer(),
    "discount":fields.Integer(),
    "quantity":fields.Integer(),
})
avatar_base_model = shop_ns.model('AvatarModel', {
    "avatarId":fields.Integer(),
    "image":fields.String(),
    "title":fields.String(),
    "description":fields.String(),
    "neededGems":fields.Integer(),
})

shop_model = shop_ns.model('ShopModel', {
    'coins':fields.Nested(coins_base_model),
    'gems':fields.Nested(gems_base_model),
    'chest':fields.Nested(chest_base_model),
    'avatars':fields.Nested(avatar_base_model),
})


@shop_ns.route('')
class Shop(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token',required=False)
    @shop_ns.header('Authorization: Bearer', 'JWT TOKEN', required=False)
    @shop_ns.doc(parser=parser,validate=True)
    @shop_ns.response(200, "Success",shop_model)
    @token_optional
    def get(self,current_user):
        cheapGems = []
        expGems = []
        coins = []
        avatars = []
        chest = {}

        chest_result = Chest.query.filter_by(is_active=True).order_by(desc(Chest.created)).first()
        avatar_price = 0
        if chest_result:
            for avatar in chest_result.avatars:
                avatar_price += avatar.needed_gems * GEMS_BASE_PRICE

            chest_main_price = float(chest_result.coin.price) + float(chest_result.gem.price) + avatar_price
            chest_discount_price =chest_main_price - chest_result.discount * (float(chest_result.coin.price) + float(chest_result.gem.price) + avatar_price)

            chest ={
                    "chestId":chest_result.id,
                    "image":chest_result.image.split("'")[1],
                    "title":chest_result.title,
                    "description":chest_result.description,
                    "discount":str(chest_result.discount * 100),
                    "price":str(chest_main_price),
                    "discountedPrice":str(chest_discount_price)
                }
        coin_result = Coin.query.filter_by(type=CoinType.FORSALE).order_by(asc(Coin.quantity))
        gem_result_cheap = Gem.query.filter(Gem.type==GemType.FORSALE,Gem.price <= 1000000).order_by(asc(Gem.quantity))
        gem_result_exp = Gem.query.filter(Gem.type==GemType.FORSALE,Gem.price > 1000000).order_by(asc(Gem.quantity))
        avatar_result = Avatar.query.filter_by(type=AvatarType.PRIVATE).order_by(asc(Avatar.needed_gems))

        for coin in coin_result:
            coins.append({
                "coinId":coin.id,
                "title":coin.title,
                "description":coin.description,
                "quantity":coin.quantity,
                "price":str(coin.price),
            })

        for gem in gem_result_cheap:
            cheapGems.append({
                "gemId":gem.id,
                "title":gem.title,
                "description":gem.description,
                "quantity":gem.quantity,
                "price":str(gem.price),
                "discount":str(gem.discount * 100),
            })

        for gem in gem_result_exp:
            expGems.append({
                "gemId":gem.id,
                "title":gem.title,
                "description":gem.description,
                "quantity":gem.quantity,
                "price":str(gem.price),
                "discount":str(gem.discount * 100),
            })

        authToken = False
        if(current_user):
            authToken = True
            for avatar in avatar_result:
                if avatar not in current_user.avatars:
                    avatars.append({
                        "avatarId":avatar.id,
                        "image":avatar.image.split("'")[1],
                        "title":avatar.title,
                        "description":avatar.description,
                        "neededGems":avatar.needed_gems
                    })
        else:
            for avatar in avatar_result:
                avatars.append({
                    "avatarId":avatar.id,
                    "image":avatar.image.split("'")[1],
                    "title":avatar.title,
                    "description":avatar.description,
                    "neededGems":avatar.needed_gems,
                    "price":avatar.needed_gems*GEMS_BASE_PRICE
                })

        return make_response(jsonify({'coins':coins,'cheapGems':cheapGems,'expGems':expGems,'chest':chest,'avatars':avatars}),200)

coin_auction_plan_model = shop_ns.model('CoinAuctionPlan', {
    "planId":fields.Integer(),
    "title":fields.String(),
    "coinCount":fields.Integer(),
    "price":fields.Integer(),
    "discountCoupon":fields.Integer(),
})

shop_auction_model = shop_ns.model('ShopAuctionModel', {
    'coinAuctionPlan':fields.Nested(coin_auction_plan_model),
    'coins':fields.Nested(coins_base_model),
    'gems':fields.Nested(gems_base_model),
    'chest':fields.Nested(chest_base_model),
    'avatars':fields.Nested(avatar_base_model),
})

register_auction_model = shop_ns.model('CoinRegisterAuction', {
    'auctionId':fields.Integer(description='The auction id', required=True),
    'planId':fields.Integer(description='The plan id', required=True),
})

@shop_ns.route('/auction')
class ShopAuction(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token',required=True)
    @shop_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @shop_ns.doc('Shop for auction api', parser=parser, body=register_auction_model, validate=False)
    @shop_ns.response(200, "Success",shop_auction_model)
    @token_required
    def post(self,current_user):
        required_fields = ['auctionId','planId']
        for key in required_fields:
            if key not in shop_ns.payload:
                for k, v in AUCTION_REGISTERـREQUIRED.items():
                    if key==k:
                        return make_response(jsonify({"success":False,"reason":k,"message":v}),400)

        auctionId = shop_ns.payload['auctionId']
        planId = shop_ns.payload['planId']
        auction = Auction.query.get(auctionId)

        if not auction:
            return make_response(jsonify({"success":False,"reason":'auctionNotFound',"message":AUCTION_PARTICIPATION['AUCTION_NOT_FOUND']}),403)

        if not auction.is_active:
            return make_response(jsonify({"success":False,"reason":'auctionNotActive',"message":AUCTION_PARTICIPATION['AUCTION_NOT_ACTIVE']}),403)

        auction_plan = AuctionPlan.query.filter_by(auction_id=auctionId, plan_id=planId).first()
        if not auction_plan:
            return make_response(jsonify({"success":False,"reason":'auctionPlanNotFound',"message":AUCTION_PARTICIPATION['AUCTION_PLAN_NOT_FOUND']}),403)

        if(auction.start_date < datetime.now()):
            return make_response(jsonify({"success":False,"reason":'auctionExpired',"message":AUCTION_PARTICIPATION['AUCTION_EXPIRED']}),403)

        if(auctionSecondsDeadline(auction.start_date) < 60):
            return make_response(jsonify({"success":False,"reason":'auctionStartSoon',"message":AUCTION_PARTICIPATION['AUCTION_DEADLINE']}),403)

        if(UserAuctionParticipation.query.filter_by(auction_id=auctionId).count() + 1 > auction.max_members):
            return make_response(jsonify({"success":False,"reason":'maxMembers',"message":AUCTION_PARTICIPATION['AUCTION_MAX_MEMBER_REACHED']}),403)

        if(current_user.level.number < auction.level.number):
            message = AUCTION_PARTICIPATION['USER_LEVEL_NOT_MEET'].replace('attribute',auction.level.title)
            return make_response(jsonify({"success":False,"reason":'level','details':{'userLevel':current_user.level.number,'auctionLevel':auction.level.number},"message":message}),403)

        if(current_user.has_auction(auction.id)):
            return make_response(jsonify({"success":False,"reason":'userAlreadyRegisteredAuction',"message":AUCTION_PARTICIPATION['AUCTION_ALREADY_REGISTERED']}),403)

        gems = []
        coins = []
        avatars = []
        chest_result = Chest.query.filter_by(is_active=True).order_by(desc(Chest.created)).first()
        chest ={
                "chestId":chest_result.id,
                "title":chest_result.title,
                "description":chest_result.description,
                "discount":str(chest_result.discount)
            }
        coin_result = Coin.query.filter_by(type=CoinType.FORSALE).order_by(desc(Coin.created))
        gem_result = Gem.query.filter_by(type=GemType.FORSALE).order_by(desc(Gem.created))
        avatar_result = Avatar.query.filter_by(type=AvatarType.PRIVATE).order_by(desc(Avatar.created))

        auction_plan = AuctionPlan.query.filter_by(auction_id=auction.id,plan_id=planId).first()
        coinAuctionPlan = {
                "planId":auction_plan.plan.id,
                "title":auction_plan.plan.title,
                "coinCount":auction_plan.needed_coins,
                "price":auction_plan.needed_coins * 1000,
                "bids":auction_plan.max_bids,
                "discountCoupon":str(auction_plan.discount),
            }
        for coin in coin_result:
            coins.append({
                "coinId":coin.id,
                "title":coin.title,
                "description":coin.description,
                "quantity":coin.quantity,
                "price":str(coin.price),
            })

        for gem in gem_result:
            gems.append({
                "gemId":gem.id,
                "title":gem.title,
                "description":gem.description,
                "quantity":gem.quantity,
                "price":str(gem.price),
                "discount":str(gem.discount),
            })

        for avatar in avatar_result:
            if avatar not in current_user.avatars:
                avatars.append({
                    "avatarId":avatar.id,
                    "image":avatar.image.split("'")[1],
                    "title":avatar.title,
                    "description":avatar.description,
                    "neededGems":avatar.needed_gems
                })

        return make_response(jsonify({"success":True,'coinAuctionPlan':coinAuctionPlan,'coins':coins,'gems':gems,'chest':chest,'avatars':avatars}),200)
