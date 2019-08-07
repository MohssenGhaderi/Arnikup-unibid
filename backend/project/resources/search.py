from flask_restplus import Resource, fields, Namespace
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session, flash
import json
from project import app, rest_api
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
import os
from sqlalchemy import and_, or_, asc,desc
from ..model.guest_message import GuestMessage
from project.utils import token_required, token_optional
from project.helpers import auctionMillisecondsDeadline
from definitions import SITE_PREFIX, COINS_BASE_PRICE, GEMS_BASE_PRICE, AUCTION_START_PROGRESS
import math

search_ns = Namespace('search')

participants_fields = search_ns.model('ParticipantsFields', {
    "icons":fields.List(fields.String),
    "count":fields.Integer()
})

charity_fields = search_ns.model('ParticipantsFields', {
    "icon":fields.String(),
    "description":fields.String()
})

status_fields = search_ns.model('ParticipantsFields', {
    "bidPrice":fields.Integer(),
    "name":fields.String(),
    "avatar":fields.String()
})

coin_fields = search_ns.model('CoinFields', {
        "planId":fields.Integer(),
        "title":fields.String(),
        "count":fields.Integer(),
        "price":fields.Integer(),
        "bids":fields.Integer(),
        "discountCoupon":fields.Integer(),
})

last_auction_base_model = search_ns.model('LastAuctionBase', {
    "charity":fields.Nested(charity_fields),
    "participants":fields.Nested(participants_fields),
    "status":fields.Nested(status_fields),
    "coins":fields.Nested(coin_fields),
    "auctionId":fields.Integer(),
    "level":fields.Integer(),
    "maxLevel":fields.Integer(),
    "maxMembers":fields.Integer(),
    'image':fields.String(),
    "liked":fields.Boolean,
    "participated":fields.Boolean,
    "tag":fields.String(),
    "title":fields.String(),
    "basePrice":fields.Integer(),
    "maxPrice":fields.Integer(),
    "discount":fields.Integer(),
    "remainedTime":fields.Integer()
})

last_auction_model = search_ns.model('LastAuctions', {
    'lastAuctions':fields.Nested(last_auction_base_model),
})

@search_ns.route('')
class SearchAuctions(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token',required=False)
    parser.add_argument('text', location='args', help='Queried text')
    parser.add_argument('categoryId', location='args', help='Queried categoryId')
    @search_ns.header('Authorization: Bearer', 'JWT TOKEN', required=False)
    @search_ns.doc(parser=parser,validate=True)
    @search_ns.response(200, "Success",last_auction_model)
    @token_optional
    def get(self,current_user):

        searchText = None
        categoryId = None

        if 'text' in request.args:
            if request.args['text'] != '':
                searchText = request.args['text']

        if 'categoryId' in request.args:
            category = Category.query.get(request.args['categoryId'])
            if category:
                categoryId = category.id

        result = []
        if searchText and categoryId:
            result = Auction.query.filter(Auction.start_date > datetime.now(),or_(Auction.title.like("%"+searchText+"%"),Item.title.like("%"+searchText+"%"))).join(Item).join(Product).join(Category).filter_by(id = categoryId).order_by(Auction.created.desc()).limit(6)
        elif not searchText and categoryId:
            result = Auction.query.filter(Auction.start_date > datetime.now()).join(Item).join(Product).join(Category).filter_by(id = categoryId).order_by(Auction.created.desc()).limit(6)
        elif not categoryId and searchText:
            result = Auction.query.filter(Auction.start_date > datetime.now(),or_(Auction.title.like("%"+searchText+"%"),Item.title.like("%"+searchText+"%"))).join(Item).order_by(Auction.created.desc()).limit(6)
        elif not categoryId and not searchText:
            result = Auction.query.filter(Auction.start_date > datetime.now()).order_by(Auction.created.desc()).limit(6)

        auctions = []
        levels = Level.query.count()

        for auction in result:
            participant_icons = []
            for participant in auction.participants:
                if avatar:
                    participant_icons.append(participant.avatar.image.split("'")[1])

            participants = {
                "icons":[],
                "count":0
            }
            charity = {}
            if auction.charity:
                charity ={
                    "icon":auction.charity.icon.split("'")[1],
                    "description":auction.charity.description
                }

            if auction.participants.count() > 0 :
                participants = {
                "icons":participant_icons,
                "count":auction.participants.count()}

            liked = False
            participated = False
            bids = 0
            if current_user:
                authToken = True
                liked = auction in current_user.auction_likes
                participated = auction in current_user.auctions

            discount = math.ceil(( (auction.item.price - auction.max_price) / auction.item.price )*100)

            coins = []
            plan = {}
            if participated :
                user_auction_plan = AuctionPlan.query.join(UserPlan).filter(AuctionPlan.auction_id==auction.id,UserPlan.user_id==current_user.id).first()
                plan  = {
                    "title":user_auction_plan.plan.title,
                    "coins":user_auction_plan.needed_coins,
                    "bids":user_auction_plan.max_bids,
                }
                user_plan = UserPlan.query.join(AuctionPlan).filter(AuctionPlan.auction_id==auction.id,UserPlan.user_id==current_user.id).first()

                my_last_bid = Bid.query.join(UserPlan).filter(UserPlan.id==user_plan.id,Bid.auction_id==auction.id).order_by(desc(Bid.created)).first()

                if my_last_bid:
                    bids = my_last_bid.current_bids
                else:
                    bids = user_auction_plan.max_bids
            else:
                auction_plan_result = AuctionPlan.query.filter_by(auction_id=auction.id).all()
                for auction_plan in auction_plan_result:
                    coins.append({
                        "planId":auction_plan.plan.id,
                        "title":auction_plan.plan.title,
                        "coinCount":auction_plan.needed_coins,
                        "price":auction_plan.needed_coins * COINS_BASE_PRICE,
                        "bids":auction_plan.max_bids,
                        "discountCoupon":str(auction_plan.discount),
                    })

            remainedTime = auctionMillisecondsDeadline(auction.start_date)
            if remainedTime < AUCTION_START_PROGRESS * 1000 :
                last_bid = Bid.query.filter_by(auction_id=auction.id).order_by(desc(Bid.created)).first()
                if last_bid :
                    status = {
                        "bidPrice":str(last_bid.bid_price),
                        "name":last_bid.user_plan.user.username,
                        "avatar":last_bid.user_plan.user.avatar.image.split("'")[1],
                        }
                    auctions.append({
                    "status":status,
                    "charity":charity,
                    "coins":coins,
                    "auctionId":auction.id,
                    "image":auction.image.split("'")[1],
                    "level":auction.level.number,
                    "maxLevel":levels,
                    "likeCount":auction.likes.count(),
                    "participants":participants,
                    "maxMembers":auction.max_members,
                    "liked":liked,
                    "participated":participated,
                    "bids":bids,
                    "plan":plan,
                    "tag":auction.tag,
                    "title":auction.title,
                    "basePrice":str(auction.base_price),
                    "maxPrice":str(auction.max_price),
                    "remainedTime":remainedTime,
                    "discount":discount,
                    })
                else:
                    auctions.append({
                    "coins":coins,
                    "charity":charity,
                    "auctionId":auction.id,
                    "image":auction.image.split("'")[1],
                    "level":auction.level.number,
                    "maxLevel":levels,
                    "likeCount":auction.likes.count(),
                    "participants":participants,
                    "maxMembers":auction.max_members,
                    "liked":liked,
                    "participated":participated,
                    "bids":bids,
                    "plan":plan,
                    "tag":auction.tag,
                    "title":auction.title,
                    "basePrice":str(auction.base_price),
                    "maxPrice":str(auction.max_price),
                    "remainedTime":remainedTime,
                    "discount":discount,
                    })

            else:
                auctions.append({
                "coins":coins,
                "charity":charity,
                "auctionId":auction.id,
                "image":auction.image.split("'")[1],
                "level":auction.level.number,
                "maxLevel":levels,
                "likeCount":auction.likes.count(),
                "participants":participants,
                "maxMembers":auction.max_members,
                "liked":liked,
                "participated":participated,
                "bids":bids,
                "plan":plan,
                "tag":auction.tag,
                "title":auction.title,
                "basePrice":str(auction.base_price),
                "maxPrice":str(auction.max_price),
                "remainedTime":remainedTime,
                "discount":discount,
                })

        return make_response(jsonify({"lastAuctions":auctions}),200)
