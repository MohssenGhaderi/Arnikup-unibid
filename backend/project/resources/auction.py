from ..model import *
from flask_restplus import Resource, fields, Namespace
from flask import url_for, redirect, request, abort, make_response , jsonify , session, flash
from project import app, rest_api
from datetime import datetime
from sqlalchemy import or_, asc
from ..model.guest_message import GuestMessage
from project.utils import token_required, token_optional
from project.helpers import *
from project.lang.fa import *
from definitions import SITE_PREFIX, COINS_BASE_PRICE, GEMS_BASE_PRICE, AUCTION_START_DEADLINE
import math

auction_ns = Namespace('auction')

#COIN operations

register_auction_model = auction_ns.model('CoinRegisterAuction', {
    'auctionId':fields.Integer(description='The auction id', required=True),
    'planId':fields.Integer(description='The plan id', required=True),
})

register_auction_not_qualified_model = auction_ns.model('AuctionRegistrationQualification', {
    'planId':fields.Integer(description='The plan id for requested auction plan', required=True),
    'coinsNeeded':fields.Integer(description='The needed coins for this auction', required=True),
    'requiredGems':fields.Integer(description='The needed gems for converting to coins', required=True),
})

register_auction_success_model = auction_ns.model('AuctionRegistrationSuccess', {
    'auction':fields.String(description='The registered auction', required=True),
    'coinsNeeded':fields.Integer(description='The needed coins for this auction', required=True),
})


@auction_ns.route('/coin/registeration')
class CoinRegisterAuction(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token',required=True)
    @auction_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @auction_ns.doc('Register for auction api', parser=parser, body=register_auction_model, validate=False)
    @auction_ns.response(200, "Success",register_auction_success_model)
    @auction_ns.response(400, "Validation and system errors")
    @auction_ns.response(401, "Not Authorized")
    @auction_ns.response(403, "Auction, plan errors and user is not qualified for auction registeration",register_auction_not_qualified_model)
    @token_required
    def post(self,current_user):
        required_fields = ['auctionId','planId']
        for key in required_fields:
            if key not in auction_ns.payload:
                for k, v in AUCTION_REGISTERـREQUIRED.items():
                    if key==k:
                        return make_response(jsonify({"success":False,"reason":k,"message":v}),400)

        auctionId = auction_ns.payload['auctionId']
        planId = auction_ns.payload['planId']
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

        if(auctionSecondsDeadline(auction.start_date) < AUCTION_START_DEADLINE):
            return make_response(jsonify({"success":False,"reason":'auctionStartSoon',"message":AUCTION_PARTICIPATION['AUCTION_DEADLINE']}),403)

        if(current_user.level.number < auction.level.number):
            message = AUCTION_PARTICIPATION['USER_LEVEL_NOT_MEET'].replace('attribute',auction.level.title)
            return make_response(jsonify({"success":False,"reason":'level','details':{'userLevel':current_user.level.number,'auctionLevel':auction.level.number},"message":message}),403)

        if(UserAuctionParticipation.query.filter_by(auction_id=auctionId).count() + 1 > auction.max_members):
            return make_response(jsonify({"success":False,"reason":'maxMembers',"message":AUCTION_PARTICIPATION['AUCTION_MAX_MEMBER_REACHED']}),403)


        if(current_user.has_auction(auction.id)):
            return make_response(jsonify({"success":False,"reason":'userAlreadyRegisteredAuction',"message":AUCTION_PARTICIPATION['AUCTION_ALREADY_REGISTERED']}),403)

        if(current_user.coins < auction_plan.needed_coins):
            needed_gems = math.ceil(auction_plan.needed_coins * COINS_BASE_PRICE / GEMS_BASE_PRICE)
            return make_response(jsonify({"success":False,'reason':'coins','details':{"coinsNeeded":auction_plan.needed_coins,"requiredGems":needed_gems,"planId":planId},"message":AUCTION_PARTICIPATION['USER_NOT_ENOUGH_COINS']}),403)


        UserPlan.query.filter_by(auction_plan_id = auction_plan.id,user_id=current_user.id).delete()
        UserAuctionParticipation.query.filter_by(auction_id=auctionId,user_id=current_user.id).delete()

        current_user.coins -= auction_plan.needed_coins

        coin_payment = CoinPayment()
        coin_payment.paid_coins = auction_plan.needed_coins
        coin_payment.type = CoinPayType.PLANCOIN
        coin_payment.status = CoinPayStatus.DONE
        coin_payment.sequence = CoinPayStatus.WAIT + ' - ' + CoinPayStatus.DONE
        coin_payment.user = current_user

        user_plan = UserPlan()
        user_plan.user = current_user
        user_plan.auction_plan = auction_plan

        user_plan_coin_payment = UserPlanCoinPayment()
        user_plan_coin_payment.user_plan = user_plan
        user_plan_coin_payment.coin_payment = coin_payment

        user_auction_participation = UserAuctionParticipation()
        user_auction_participation.user = current_user
        user_auction_participation.auction_id = auctionId

        title = str(auction.title).replace('حراجی','')
        message = str(current_user) + ' عزیز ٬' \
        + '\n' + 'مجوز شرکت در حراجی برای شما صادر گردید.'\
        + '\n' + 'یونی بید'\
        + '\n' + 'www.unibid.ir'

        auction_notification = SiteNotification()
        auction_notification.title = 'مجوز شرکت در حراجی'
        auction_notification.text = 'مجوز شرکت در حراجی ' + title + 'برای شما صادر گردید'
        auction_notification.sms = message
        auction_notification.link = SITE_PREFIX+'/view/auction/'+str(auction.id)
        auction_notification.details = str(current_user)
        auction_notification.type = SiteNotificationType.PARTICIPATE
        auction_notification.user = current_user

        user_activity = UserActivity()
        user_activity.user = current_user
        user_activity.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        user_activity.activity = ACTIVITIES['AUCTION']

        db.session.add(coin_payment)
        db.session.add(user_plan)
        db.session.add(user_plan_coin_payment)
        db.session.add(user_auction_participation)
        db.session.add(current_user)
        db.session.add(auction_notification)
        db.session.add(user_activity)
        db.session.commit()

        return make_response(jsonify({"success":True,'details':{"coinsNeeded":auction_plan.needed_coins,"auction":auction.title},"message":AUCTION_PARTICIPATION['PLAN_SUCCESS']}),200)

#GEM operations

register_auction_gem_model = auction_ns.model('GemRegisterAuction', {
    'auctionId':fields.Integer(description='The auction id', required=True),
    'planId':fields.Integer(description='The plan id', required=True),
})

@auction_ns.route('/gem/registeration')
class GemRegisterAuction(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token',required=True)
    @auction_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @auction_ns.doc('Register for auction api', parser=parser, body=register_auction_model, validate=False)
    @auction_ns.response(200, "Success")
    @auction_ns.response(400, "Validation and system errors")
    @auction_ns.response(401, "Not Authorized")
    @auction_ns.response(403, "User is not qualified for auction registeration")
    @token_required
    def post(self,current_user):
        required_fields = ['auctionId','planId']
        for key in required_fields:
            if key not in auction_ns.payload:
                for k, v in AUCTION_REGISTERـREQUIRED.items():
                    if key==k:
                        return make_response(jsonify({"success":False,"reason":k,"message":v}),400)

        auctionId = auction_ns.payload['auctionId']
        planId = auction_ns.payload['planId']
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

        needed_gems = math.ceil(auction_plan.needed_coins * COINS_BASE_PRICE / GEMS_BASE_PRICE)
        if(current_user.gems < needed_gems):
            return make_response(jsonify({"success":False,"reason":'redirectShop',"message":AUCTION_PARTICIPATION['USER_NOT_ENOUGH_GEMS']}),403)

        UserPlan.query.filter_by(auction_plan_id = auction_plan.id,user_id=current_user.id).delete()
        UserAuctionParticipation.query.filter_by(auction_id=auctionId,user_id=current_user.id).delete()

        current_user.gems -= needed_gems
        paid_coins = math.ceil(((needed_gems * GEMS_BASE_PRICE) - (auction_plan.needed_coins * COINS_BASE_PRICE)) / COINS_BASE_PRICE)
        current_user.coins += paid_coins

        gem_payment = GemPayment()
        gem_payment.paid_gems = needed_gems
        gem_payment.type = GemPayType.BUYPLAN
        gem_payment.status = GemPayStatus.DONE
        gem_payment.sequence = GemPayStatus.WAIT + ' - ' + GemPayStatus.DONE
        gem_payment.user = current_user

        coin_payment = CoinPayment()
        coin_payment.paid_coins = paid_coins
        coin_payment.type = CoinPayType.GEMFRACTION
        coin_payment.status = CoinPayStatus.DONE
        coin_payment.sequence = CoinPayStatus.WAIT + ' - ' + CoinPayStatus.DONE
        coin_payment.user = current_user

        user_plan = UserPlan()
        user_plan.user = current_user
        user_plan.auction_plan = auction_plan

        user_plan_gem_payment = UserPlanGemPayment()
        user_plan_gem_payment.user_plan = user_plan
        user_plan_gem_payment.gem_payment = gem_payment

        user_auction_participation = UserAuctionParticipation()
        user_auction_participation.user = current_user
        user_auction_participation.auction_id = auctionId

        title = str(auction.title).replace('حراجی','')
        message = str(current_user) + ' عزیز ٬' \
        + '\n' + 'مجوز شرکت در حراجی برای شما صادر گردید.'\
        + '\n' + 'یونی بید'\
        + '\n' + 'www.unibid.ir'

        auction_notification = SiteNotification()
        auction_notification.title = 'مجوز شرکت در حراجی'
        auction_notification.text = ' مجوز شرکت در حراجی ' + title + ' برای شما صادر گردید '
        auction_notification.sms = message
        auction_notification.link = SITE_PREFIX+'/view/auction/'+str(auction.id)
        auction_notification.details = str(current_user)
        auction_notification.type = SiteNotificationType.PARTICIPATE
        auction_notification.user = current_user

        user_activity = UserActivity()
        user_activity.user = current_user
        user_activity.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        user_activity.activity = ACTIVITIES['AUCTION']

        db.session.add(coin_payment)
        db.session.add(gem_payment)
        db.session.add(user_plan)
        db.session.add(user_plan_gem_payment)
        db.session.add(user_auction_participation)
        db.session.add(current_user)
        db.session.add(auction_notification)
        db.session.add(user_activity)
        db.session.commit()

        return make_response(jsonify({"success":True,'details':{"paidGems":needed_gems,"coinsFraction":paid_coins,"coinsNeeded":auction_plan.needed_coins,"auction":auction.title},"message":AUCTION_PARTICIPATION['PLAN_SUCCESS']}),200)


like_auction_model = auction_ns.model('LikeAuction', {
    'auctionId':fields.Integer(description='The auction id', required=True),
})

#LIKE operations

@auction_ns.route('/like')
class LikeAuction(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token',required=True)
    @auction_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @auction_ns.doc('Register for auction api', parser=parser, body=like_auction_model, validate=False)
    @auction_ns.response(200, "Success")
    @auction_ns.response(400, "Validation and system errors")
    @auction_ns.response(401, "Not Authorized")
    @auction_ns.response(403, "User is not qualified for auction registeration")
    @token_required
    def post(self,current_user):

        if 'auctionId' not in auction_ns.payload:
            return make_response(jsonify({"success":False,"reason":'auctionId',"message":AUCTION['REQUIRED']}),400)

        auction = Auction.query.get(auction_ns.payload['auctionId'])
        if not auction :
            return make_response(jsonify({"success":False,"reason":'auctionId',"message":AUCTION['NOT_FOUND']}),400)

        message = ''

        if(auction not in current_user.auction_likes):
            user_activity = UserActivity()
            user_activity.user = current_user
            user_activity.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            user_activity.activity = ACTIVITIES['AUCTION_LIKE'].replace('attribute',auction.title)
            db.session.add(user_activity)
            db.session.commit()

            message = AUCTION['LIKE'].replace('attribute',auction.title)
            current_user.auction_likes.append(auction)

        else:
            current_user.auction_likes.remove(auction)
            message = AUCTION['DISLIKE'].replace('attribute',auction.title)
            user_activity = UserActivity()
            user_activity.user = current_user
            user_activity.ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            user_activity.activity = ACTIVITIES['AUCTION_DIS_LIKE'].replace('attribute',auction.title)
            db.session.add(user_activity)
            db.session.commit()


        db.session.add(current_user)
        db.session.commit()
        return make_response(jsonify({"success":True,"message":message}),200)