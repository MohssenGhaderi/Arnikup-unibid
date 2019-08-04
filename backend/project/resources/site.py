from flask_restplus import Resource, fields, Namespace
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session, flash
import json
from project import app, rest_api
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
import os
from sqlalchemy import or_, asc,desc
from ..model.guest_message import GuestMessage
from project.utils import token_required, token_optional
from project.helpers import auctionMillisecondsDeadline
from definitions import SITE_PREFIX, COINS_BASE_PRICE, GEMS_BASE_PRICE, AUCTION_START_PROGRESS
import math

site_ns = Namespace('site')

participants_fields = site_ns.model('ParticipantsFields', {
    "icons":fields.List(fields.String),
    "count":fields.Integer()
})

slider_auction_base_model = site_ns.model('SliderAuctionBase', {
    'image':fields.String(),
    "likeCount":fields.Integer(),
    "participants":fields.Nested(participants_fields),
    "auctionId":fields.Integer(),
    "maxMembers":fields.Integer(),
    "liked":fields.Boolean,
    "participated":fields.Boolean,
    "tag":fields.String(),
    "title":fields.String(),
    "basePrice":fields.Integer(),
    "maxPrice":fields.Integer(),
    "remainedTime":fields.Integer()
})

slider_auction_model = site_ns.model('SliderAuctions', {
    'sliderAuctions':fields.Nested(slider_auction_base_model),
})

@site_ns.route('/slider/auctions')
class SliderAuctions(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token',required=False)
    @site_ns.header('Authorization: Bearer', 'JWT TOKEN', required=False)
    @site_ns.doc(parser=parser,validate=True)
    @site_ns.response(200, "Success",slider_auction_model)
    @token_optional
    def get(self,current_user):
        authToken = False
        result = Auction.query.join(Advertisement).filter(Auction.start_date > datetime.now(),Auction.is_active==True).order_by(asc(Auction.start_date))
        auctions = []
        for auction in result:
            participant_icons = []
            for participant in auction.participants:
                if avatar:
                    participant_icons.append(participant.avatar.image.split("'")[1])

            participants = {
                "icons":[],
                "count":0
            }

            if auction.participants.count() > 0 :
                participants = {
                "icons":participant_icons,
                "count":auction.participants.count()}

            liked = False
            participated = False

            if current_user:
                authToken = True
                liked = auction in current_user.auction_likes
                participated = auction in current_user.auctions

            auctions.append({
            "auctionId":auction.id,
            "image":auction.advertisement.image.split("'")[1],
            "likeCount":auction.likes.count(),
            "participants":participants,
            "maxMembers":auction.max_members,
            "liked":liked,
            "participated":participated,
            "tag":auction.tag,
            "title":auction.title,
            "basePrice":str(auction.base_price),
            "maxPrice":str(auction.max_price),
            "remainedTime":auctionMillisecondsDeadline(auction.start_date),
            })


        return make_response(jsonify({"success":True,"authToken":authToken,"sliderAuctions":auctions}),200)

charity_fields = site_ns.model('ParticipantsFields', {
    "icon":fields.String(),
    "description":fields.String()
})

status_fields = site_ns.model('ParticipantsFields', {
    "lastBidPrice":fields.Integer(),
    "winnerName":fields.String(),
    "winnerAvatar":fields.String()
})

coin_fields = site_ns.model('CoinFields', {
        "planId":fields.Integer(),
        "title":fields.String(),
        "count":fields.Integer(),
        "price":fields.Integer(),
        "bids":fields.Integer(),
        "discountCoupon":fields.Integer(),
})

last_auction_base_model = site_ns.model('LastAuctionBase', {
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

last_auction_model = site_ns.model('LastAuctions', {
    'lastAuctions':fields.Nested(last_auction_base_model),
})

@site_ns.route('/last/auctions')
class LastAuctions(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token',required=False)
    @site_ns.header('Authorization: Bearer', 'JWT TOKEN', required=False)
    @site_ns.doc(parser=parser,validate=True)
    @site_ns.response(200, "Success",last_auction_model)
    @token_optional
    def get(self,current_user):
        result = Auction.query.filter(Auction.start_date > datetime.now(),Auction.advertisement==None,Auction.is_active==True).order_by(asc(Auction.start_date))
        auctions = []
        levels = Level.query.count()
        authToken = False

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
                        "lastBidPrice":str(last_bid.bid_price),
                        "winnerName":last_bid.user_plan.user.username,
                        "winnerAvatar":last_bid.user_plan.user.avatar.image.split("'")[1],
                        }
                    auctions.append({
                    "status":status,
                    "charity":charity,
                    "coins":coins,
                    "auctionId":auction.id,
                    "image":auction.item.images.split("'")[1],
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
                    "image":auction.item.images.split("'")[1],
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
                "image":auction.item.images.split("'")[1],
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

        return make_response(jsonify({"success":True,"authToken":authToken,"lastAuctions":auctions}),200)


category_fields = site_ns.model('Category', {
    "categoryId":fields.Integer(),
    "title":fields.String(),
    "icon":fields.String()
})

categories_model = site_ns.model('Categories', {
    'categories':fields.Nested(category_fields),
})

@site_ns.route('/categories')
class Categories(Resource):
    @site_ns.response(200, "Success",categories_model)
    def get(self):
        result = Category.query.all()
        categories = []
        for category in result:
            if len(category.icon)>2:
                categories.append({
                "categoryId":category.id,
                "title":category.title,
                "icon":category.icon.split("'")[1],
                })
        return make_response(jsonify({"categories":categories}),200)
