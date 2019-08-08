from flask_restplus import Resource, fields, Namespace
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session, flash
import json
from project import app, db, rest_api
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
import re
from project.lang.fa import *

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
    parser.add_argument('start', location='args', help='starting point')
    parser.add_argument('stop', location='args', help='stopping point')
    @site_ns.header('Authorization: Bearer', 'JWT TOKEN', required=False)
    @site_ns.doc(parser=parser,validate=True)
    @site_ns.response(200, "Success",slider_auction_model)
    @token_optional
    def get(self,current_user):
        start = 0
        stop = 3
        if 'start' in request.args:
            if request.args['start'] != '':
                start = int(request.args['start'])

        if 'stop' in request.args:
            if request.args['stop'] != '':
                stop = int(request.args['stop'])

        result = Auction.query.join(Advertisement).filter(Auction.start_date > datetime.now(),Auction.is_active==True).order_by(asc(Auction.start_date))
        lastAuctions = Auction.query.filter(Auction.start_date > datetime.now(),Auction.is_active==True).order_by(asc(Auction.start_date)).slice(start,stop)

        auctions = []
        for auction in lastAuctions:
            if auction in result:
                participant_icons = []
                for participant in auction.participants.order_by(UserAuctionParticipation.created.desc()).limit(6):
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

        if start == 0 and stop == 3:
            total = Auction.query.join(Advertisement).filter(Auction.start_date > datetime.now(),Auction.is_active==True).count()
            return make_response(jsonify({"success":True,"total":total,"sliderAuctions":auctions}),200)

        return make_response(jsonify({"success":True,"sliderAuctions":auctions}),200)

charity_fields = site_ns.model('ParticipantsFields', {
    "icon":fields.String(),
    "description":fields.String()
})

status_fields = site_ns.model('ParticipantsFields', {
    "bidPrice":fields.Integer(),
    "name":fields.String(),
    "avatar":fields.String()
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
    parser.add_argument('start', location='args', help='starting point')
    parser.add_argument('stop', location='args', help='stopping point')
    @site_ns.header('Authorization: Bearer', 'JWT TOKEN', required=False)
    @site_ns.doc(parser=parser,validate=True)
    @site_ns.response(200, "Success",last_auction_model)
    @token_optional
    def get(self,current_user):
        start = 0
        stop = 3
        if 'start' in request.args:
            if request.args['start'] != '':
                start = int(request.args['start'])

        if 'stop' in request.args:
            if request.args['stop'] != '':
                stop = int(request.args['stop'])


        result = Auction.query.filter(Auction.start_date > datetime.now(),Auction.is_active==True).order_by(asc(Auction.start_date)).slice(start,stop)
        auctions = []
        levels = Level.query.count()
        authToken = False

        for auction in result:
            participant_icons = []
            for participant in auction.participants.order_by(UserAuctionParticipation.created.desc()).limit(3):
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

            charity = {}
            if auction.charity:
                charity ={
                    "icon":auction.charity.icon.split("'")[1],
                    "description":auction.charity.description
                }

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

        if start == 0 and stop == 3:
            total = Auction.query.filter(Auction.start_date > datetime.now(),Auction.is_active==True).count()
            return make_response(jsonify({"success":True,"authToken":authToken,"total":total,"lastAuctions":auctions}),200)

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


finished_auction_base_model = site_ns.model('FinishedAuctionBase', {
    "status":fields.Nested(status_fields),
    "auctionId":fields.Integer(),
    "level":fields.Integer(),
    "maxLevel":fields.Integer(),
    "maxMembers":fields.Integer(),
    "totalParticipants":fields.Integer(),
    'image':fields.String(),
    "liked":fields.Boolean,
    "participated":fields.Boolean,
    "title":fields.String(),
    "basePrice":fields.Integer(),
    "maxPrice":fields.Integer(),
    "discount":fields.Integer(),
    "date":fields.String()
})

finished_auction_model = site_ns.model('FinishedAuctions', {
    'finishedAuctions':fields.Nested(finished_auction_base_model),
})

@site_ns.route('/finished/auctions')
class FinishedAuctions(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token',required=False)
    @site_ns.header('Authorization: Bearer', 'JWT TOKEN', required=False)
    @site_ns.doc(parser=parser,validate=True)
    @site_ns.response(200, "Success",finished_auction_model)
    @token_optional
    def get(self,current_user):
        result = Auction.query.filter(Auction.start_date < datetime.now(),Auction.done==True).order_by(Auction.start_date.desc())
        auctions = []
        levels = Level.query.count()

        for auction in result:
            participant_icons = []

            winnerBid = Bid.query.filter_by(auction_id=auction.id,won=True).order_by(Bid.created.desc()).first()

            liked = False
            participated = False
            bids = 0
            if current_user:
                liked = auction in current_user.auction_likes
                participated = auction in current_user.auctions

            discount = math.ceil(((auction.item.price - winnerBid.bid_price) / auction.item.price )*100)

            status = {
                "bidPrice":str(winnerBid.bid_price),
                "name":winnerBid.user_plan.user.username,
                "avatar":winnerBid.user_plan.user.avatar.image.split("'")[1],
                }
            auctions.append({
            "status":status,
            "auctionId":auction.id,
            "image":auction.image.split("'")[1],
            "level":auction.level.number,
            "maxLevel":levels,
            "liked":liked,
            "participated":participated,
            "title":auction.title,
            "basePrice":str(auction.base_price),
            "maxPrice":str(winnerBid.bid_price),
            "date":str(winnerBid.updated),
            "discount":discount,
            "maxMembers":auction.max_members,
            "totalParticipants":auction.participants.count(),
            })

        return make_response(jsonify({"lastAuctions":auctions}),200)




guest_message_model = site_ns.model('GuestMessageModel', {
    "fullName":fields.String(),
    "email":fields.String(),
    "mobile":fields.String(),
    "sendType":fields.String(),
    "message":fields.String()
})


@site_ns.route('/guest/message')
class GuestMessages(Resource):
    @site_ns.doc('post guest messages api.',body=guest_message_model)
    @site_ns.response(200, 'Success')
    @site_ns.response(401, 'Not Authorized')
    @site_ns.response(403, 'Not available')
    def post(self):

        required_fields = ['fullName','sendType','message']

        for key in required_fields:
            if key not in site_ns.payload:
                for k, v in GUEST_MESSAGE_REQUIRED.items():
                    if key==k:
                        return make_response(jsonify({"success":False,"reason":k,"message":v}),400)

        if 'mobile' not in site_ns.payload and 'email' not in site_ns.payload:
                return make_response(jsonify({"success":False,"reason":'mobileOrEmail',"message":GUEST_MESSAGE_REQUIRED['mobile']}),400)


        if len(site_ns.payload['fullName']) < 3 or len(site_ns.payload['fullName']) > 128:
            return make_response(jsonify({"success":False,"reason":"fullName","message":GUEST_MESSAGE_VALIDATION['fullName']}),400)

        if len(site_ns.payload['message']) < 8 or len(site_ns.payload['message']) > 2048:
            return make_response(jsonify({"success":False,"reason":"message","message":GUEST_MESSAGE_VALIDATION['message']}),400)

        if site_ns.payload['sendType'] not in ['موبایل','ایمیل']:
            return make_response(jsonify({"success":False,"reason":'sendType',"message":GUEST_MESSAGE_VALIDATION['sendType']}),400)

        mobile = None
        if 'mobile' in site_ns.payload:
            if not str(site_ns.payload['mobile']).isdigit():
                return make_response(jsonify({"success":False,"reason":'mobile',"mobile":GUEST_MESSAGE_VALIDATION['mobile']}),400)

            if len(site_ns.payload['mobile']) > 13 or len(site_ns.payload['mobile']) < 11:
                return make_response(jsonify({"success":False,"reason":'mobile',"message":GUEST_MESSAGE_VALIDATION['mobile']}),400)

            mobile = site_ns.payload['mobile']

        email = None
        if 'email' in site_ns.payload:
            if not re.fullmatch('[^@]+@[^@]+\.[^@]+',site_ns.payload['email']):
                return make_response(jsonify({"success":False,"reason":'email',"message":GUEST_MESSAGE_VALIDATION['email']}),400)

            email = site_ns.payload['email']


        if(GuestMessage.query.filter_by(ip=request.environ.get('HTTP_X_REAL_IP', request.remote_addr))).count() < 10 :
            guest_message = GuestMessage()
            guest_message.full_name = site_ns.payload['fullName']
            guest_message.mobile = mobile
            guest_message.email = email
            guest_message.send_type = site_ns.payload['sendType']
            guest_message.message = site_ns.payload['message']
            guest_message.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            db.session.add(guest_message)
            db.session.commit()
            return make_response(jsonify({"success":True,"message":SUCCESS_MESSAGE}),200)
        else:
            return make_response(jsonify({"success":False,"message":BAN_MESSAGE}),403)
