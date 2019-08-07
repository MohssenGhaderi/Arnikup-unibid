from flask_restful import Resource, reqparse
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app
from datetime import datetime
import time
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_login import login_required ,current_user
from decimal import Decimal
import random
from definitions import COUPONCODE,MAX_INVITOR_POLICY,SITE_PREFIX
from ..melipayamak import SendMessage

class AuctionTestJson(Resource):
    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        auction_id = data['auction_id']
        # auction = Auction.query.get(auction_id)
        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('offers.created_at DESC').first()
        result = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(auction_id=auction_id).order_by('offers.created_at DESC')
        users = []
        for user in result:
            user_plan = UserPlan.query.filter_by(user_id=user.id,auction_id=auction_id).first()
            user_last_offer = Offer.query.filter_by(user_plan_id=user_plan.id,auction_id=auction_id).order_by('offers.created_at DESC').first()
            current_bids = user_last_offer.current_bids
            current_offer_price = user_last_offer.total_price
            pretty_name = user.first_name + " " + user.last_name if (user.first_name and user.last_name) else user.username
            users.append({
                "current_bids" : current_bids,
                "current_offer_price" : int(current_offer_price),
                "pretty_name" : pretty_name ,
                "avatar" : user.avatar,
                "id":user.id
            })

        user_schema = UserSchema(many=True)
        return make_response(jsonify({"success":True, "current_offer_price": str(last_offer.total_price),"users": users}),200)

class AuctionTest(Resource):
    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        auction_id = data['auction_id']
        # auction = Auction.query.get(auction_id)
        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('offers.created_at DESC').first()
        result = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(auction_id=auction_id).order_by('offers.created_at DESC')
        users = []
        for user in result:
            user_plan = UserPlan.query.filter_by(user_id=user.id,auction_id=auction_id).first()
            user_last_offer = Offer.query.filter_by(user_plan_id=user_plan.id,auction_id=auction_id).order_by('offers.created_at DESC').first()
            user.current_bids = user_last_offer.current_bids
            user.current_offer_price = user_last_offer.total_price
            users.append(user)

        user_schema = UserSchema(many=True)

        return make_response(jsonify({"success":True, "current_offer_price": str(last_offer.total_price),"users": user_schema.dump(users)}),200)

class AuctionUserViewed(Resource):
    def get(self):
        if(current_user.is_authenticated):
            result = Auction.query.join(user_auction_views).filter_by(user_id=current_user.id).order_by('user_auction_views.date DESC').limit(10)
            auctions = []
            for auction in result:
                auction_participants = []
                for participant in auction.participants:
                    auction_participants.append({"id":participant.id,"username":participant.username})
                title = auction.title
                if (len(auction.title) > 15):
                    title = auction.title[:15]+"..."
                auctions.append({
                "id":auction.id,
                "title":title,
                "images":auction.item.images,
                "base_price":str(auction.base_price),
                "participants":auction_participants,
                })
            return make_response(jsonify(auctions),200)

class AuctionViewFinished(Resource):
    def get(arg):
        return make_response(jsonify({"finished":Offer.query.filter_by(win=True).count()}),200)

    def put(self):
        data = request.get_json(force=True)
        start = data['start']
        stop = data['stop']
        result = Offer.query.filter_by(win=True).order_by("created_at DESC").slice(start,stop)
        offers = []
        for offer in result:
            user = User.query.join(UserPlan).join(Offer).filter_by(id=offer.id).first()
            if user:
                winner = ""
                if(user.first_name and user.last_name and offer.win):
                    winner = user.first_name + ' ' + user.last_name
                else:
                    winner = user.username

                offers.append({
                "auction_id":offer.auction.id,
                "title":offer.auction.title,
                "images":offer.auction.item.images,
                "total_price":int(offer.total_price),
                "main_price":int(offer.auction.item.price),
                "start_date":offer.auction.start_date,
                "participants":offer.auction.participants.count(),
                "winner":winner,
                })
        return make_response(jsonify(offers),200)

class AuctionUserParticipation(Resource):
    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        plan_id = int(data.get("plan_id", None))
        auction_id = int(data.get("auction_id", None))
        method_id = int(data.get("method_id", None))

        plan = Plan.query.join(AuctionPlan).filter_by(id=plan_id).first()
        if not plan:
            return make_response(jsonify({'success':False,"reason":"پلن درخواستی شما موجود نیست"}),400)

        auction_plan = AuctionPlan.query.filter_by(plan_id=plan.id,auction_id=auction_id).first()

        if not auction_plan:
            return make_response(jsonify({'success':False,"reason":"پلن حراجی مورد نظر شما معتبر نیست"}),400)


        payment_method = PaymentMethod.query.get(method_id)

        if not payment_method:
            return make_response(jsonify({'success':False,"reason":"روش پرداخت انتخابی شما موجود نیست"}),400)

        auction = auction_plan.auction
        now = datetime.now()
        remained = (auction.start_date - now).seconds

        if(UserAuctionParticipation.query.filter_by(auction_id=auction_id).count() + 1 > auction.max_members):
            return make_response(jsonify({'success':False,"reason":"سقف شرکت در این حراجی پر شده است"}),400)

        if(auction.start_date < now):
            return make_response(jsonify({'success':False,"reason":"زمان شرکت در حراجی منقضی شده است"}),400)

        if(remained < 60):
            return make_response(jsonify({'success':False,"reason":"حداکثر تا یک دقیقه قبل از حراجی برای ثبت نام فرصت دارید"}),400)

        UserPlan.query.filter_by(auction_plan_id = auction_plan.id,user_id=current_user.id,auction_id=auction.id).delete()
        UserAuctionParticipation.query.filter_by(auction_id=auction_id,user_id=current_user.id).delete()
        amount = auction_plan.price

        if(payment_method.type == Payment_Types.Credit):
            if amount == 0 :
                payment = Payment()
                payment.type = PaymentType.FREE
                payment.ref_id = random.randint(10000,100000)
                payment.sale_order_id = random.randint(10000,100000)
                payment.sale_refrence_id = random.randint(10000,100000)
                payment.amount = amount
                payment.discount = 0
                payment.payment_method = payment_method
                payment.status = PaymentStatus.ARCHIVE

                user_plan = UserPlan()
                user_plan.auction = auction
                user_plan.auction_plan = auction_plan
                user_plan.payment = payment

                current_user.payments.append(payment)
                current_user.auctions.append(auction)
                current_user.user_plans.append(user_plan)

                db.session.add(current_user)
                db.session.commit()

                title = str(auction.title).replace('حراجی','')
                message = str(current_user) + ' عزیز ٬' \
                + '\n' + 'مجوز شرکت در حراجی برای شما صادر گردید.'\
                + '\n' + 'یونی بید'\
                + '\n' + 'www.unibid.ir'

                auction_notification = SiteNotification()
                auction_notification.title = 'مجوز شرکت در حراجی'
                auction_notification.text = 'مجوز شرکت در حراجی ' + title + 'برای شما صادر گردید'
                auction_notification.sms = message
                auction_notification.link = SITE_PREFIX+'/auction/'+str(auction.id)
                auction_notification.details = str(current_user)
                # auction_notification.details = str(current_user)+";"+title+";"+SITE_PREFIX+'/auction/'+str(auction.id)
                auction_notification.type = SiteNotificationType.PARTICIPATE
                auction_notification.user = current_user
                db.session.add(auction_notification)
                db.session.commit()


                msg = "شما بصورت رایگان در این حراجی شرکت داده شدید"
                return make_response(jsonify({"success":True,"type":"registered","message":msg}),200)

            if(current_user.credit < amount):
                msg = "موجودی حساب شما برای پرداخت این پلن کافی نمی باشد"
                return make_response(jsonify({'success':False,"reason":msg}),400)

            payment = Payment()
            payment.type = PaymentType.PLAN
            payment.ref_id = current_user.id
            payment.sale_order_id = current_user.id
            payment.sale_refrence_id = current_user.id
            payment.amount = amount
            payment.discount = 0
            payment.payment_method = payment_method
            payment.status = PaymentStatus.ARCHIVE

            user_plan = UserPlan()
            user_plan.auction = auction
            user_plan.auction_plan = auction_plan
            user_plan.payment = payment

            current_user.payments.append(payment)
            current_user.auctions.append(auction)
            current_user.user_plans.append(user_plan)
            current_user.credit -= Decimal(amount)

            db.session.add(current_user)
            db.session.commit()

            # already_invited = current_user.gifts.filter_by(title=COUPONCODE).first()
            # if not already_invited and current_user.invitor and User.query.filter_by(invitor=current_user.invitor).count() < MAX_INVITOR_POLICY:
            #     gift = Gift.query.filter_by(title=COUPONCODE).first()
            #     if gift and not gift.expired:
            #
            #         g_payment = Payment()
            #         g_payment.amount = gift.amount
            #         g_payment.discount = 0
            #         g_payment.status = PaymentStatus.PAID
            #         g_payment.type = PaymentType.INVITOR_GIFT
            #         g_payment.payment_method = PaymentMethod.query.filter_by(title='بدون پرداخت').first()
            #         g_payment.user = current_user
            #         db.session.add(g_payment)
            #         db.session.commit()
            #
            #         current_user.gifts.append(gift)
            #         current_user.credit += Decimal(gift.amount)
            #         db.session.add(current_user)
            #         db.session.commit()
            #
            #         title = str(auction.title).replace('حراجی','')
            #         message = str(current_user) + ' عزیز ٬'\
            #         + '\n' + 'با شرکت شما در حراجی ' + title + ' کیف پول شما به میزان ' + str(int(gift.amount)) + ' تومان شارژ شد.'\
            #         + '\n' + 'با دعوت از دوستان خود با شرکت آنها در اولین حراجی هدیه معرفی خود را دریافت کنید.'\
            #         + '\n' + 'با آرزوی موفقیت و شادکامی شما'\
            #         + '\n' + 'یونی بید'\
            #         + '\n' + 'www.unibid.ir'
            #
            #         auction_notification = SiteNotification()
            #         auction_notification.title = 'دریافت هدیه دعوت از دوستان'
            #         auction_notification.text = 'جهت هدیه معرفی دوستان به یونی بید٬ کیف پول شما به میزان' + str(int(gift.amount)) + ' تومان شارژ شد.'
            #         auction_notification.sms = message
            #         auction_notification.link = SITE_PREFIX+'/profile'
            #         auction_notification.details = str(current_user)+";"+title+";"+str(int(gift.amount))
            #         auction_notification.type = SiteNotificationType.INVITORGIFT
            #         auction_notification.user = current_user
            #         db.session.add(auction_notification)
            #         db.session.commit()
            #
            #         invitor = User.query.filter_by(username=current_user.invitor).first()
            #         if invitor:
            #
            #             g_payment = Payment()
            #             g_payment.amount = gift.amount
            #             g_payment.discount = 0
            #             g_payment.status = PaymentStatus.PAID
            #             g_payment.type = PaymentType.INVITOR_GIFT
            #             g_payment.payment_method = PaymentMethod.query.filter_by(title='بدون پرداخت').first()
            #             g_payment.user = invitor
            #             db.session.add(g_payment)
            #             db.session.commit()
            #
            #             invitor.credit += Decimal(gift.amount)
            #             db.session.add(invitor)
            #             db.session.commit()
            #
            #             title = str(auction.title).replace('حراجی','')
            #             remained_invitation_coupons = MAX_INVITOR_POLICY - User.query.filter_by(invitor=invitor.username).count()
            #             message = str(invitor) + ' عزیز ٬'\
            #             + '\n' + 'با شرکت کردن '+ str(current_user) +' در حراجی '+ title + ' کیف پول شما به میزان ' + str(int(gift.amount)) + ' تومان جهت معرفی ایشان شارژ شد.'\
            #             + '\n' + ' با دعوت از '+str(remained_invitation_coupons)+' نفر دیگر از دوستان خود می توانید شارژ هدیه معرفی را دریافت کنید'\
            #             + '\n' + 'با آرزوی موفقیت و شادکامی شما'\
            #             + '\n' + 'یونی بید'\
            #             + '\n' + 'www.unibid.ir'
            #
            #             auction_notification = SiteNotification()
            #             auction_notification.title = 'دریافت هدیه دعوت از دوستان'
            #             auction_notification.text = 'جهت هدیه معرفی دوستان به یونی بید٬ کیف پول شما به میزان ' + str(int(gift.amount)) + ' تومان شارژ شد.'\
            #             + '\n' + ' با دعوت از '+str(remained_invitation_coupons)+' نفر دیگر از دوستان خود می توانید شارژ هدیه معرفی را دریافت کنید.'
            #             auction_notification.sms = message
            #             auction_notification.link = SITE_PREFIX+'/profile'
            #             auction_notification.details = str(invitor)+";"+str(current_user)+";"+title+";"+str(int(gift.amount))+";"+str(remained_invitation_coupons)
            #             auction_notification.type = SiteNotificationType.INVITORSELFGIFT
            #             auction_notification.user = invitor
            #             db.session.add(auction_notification)
            #             db.session.commit()

            title = str(auction.title).replace('حراجی','')
            message = str(current_user) + ' عزیز ٬' \
            + '\n' + 'مجوز شرکت در حراجی برای شما صادر گردید.'\
            + '\n' + 'یونی بید'\
            + '\n' + 'www.unibid.ir'

            auction_notification = SiteNotification()
            auction_notification.title = 'مجوز شرکت در حراجی'
            auction_notification.text = 'مجوز شرکت در حراجی ' + title + 'برای شما صادر گردید'
            auction_notification.sms = message
            auction_notification.link = SITE_PREFIX+'/auction/'+str(auction.id)
            auction_notification.details = str(current_user)
            auction_notification.type = SiteNotificationType.PARTICIPATE
            auction_notification.user = current_user
            db.session.add(auction_notification)
            db.session.commit()

            msg = "شرکت در حراجی با موفقیت انجام شد"
            return make_response(jsonify({"success":True,"type":"registered","message":msg}),200)

        if(payment_method.type == Payment_Types.Online):

            payment = Payment()
            payment.amount = amount
            payment.type = PaymentType.PLAN
            payment.payment_method = payment_method
            payment.status = PaymentStatus.UNPAID
            payment.discount = 0

            user_plan = UserPlan()
            user_plan.auction = auction
            user_plan.auction_plan = auction_plan
            user_plan.payment = payment

            db.session.add(user_plan)
            db.session.commit()

            current_user.payments.append(payment)
            current_user.user_plans.append(user_plan)

            db.session.add(current_user)
            db.session.commit()

            msg = " برای پرداخت به صفحه تایید هدایت می شوید"
            return make_response(jsonify({'success':True,"type":"redirect_to_bank","pid":payment.id,"message":msg}),200)

class AuctionInstanceView(Resource):
    def get(self,aid):
        auction = Auction.query.get(aid)
        auction_participants = []
        for participant in auction.participants.order_by('created_at'):
            pretty_name = participant.first_name + " " + participant.last_name if (participant.first_name and participant.last_name) else participant.username
            auction_participants.append({"id":participant.id,"pretty_name":pretty_name,"avatar":participant.avatar})

        now = datetime.now()
        days = (auction.start_date - now).days
        sign = lambda x: (1, -1)[x < 0]
        remained_time = sign(days) *  (auction.start_date - now).seconds

        plan = None
        if(current_user.is_authenticated):
            plan = AuctionPlan.query.join(UserPlan).filter_by(user_id=current_user.id,auction_id=aid).first()
        result = None

        liked = None
        if current_user.is_authenticated:
            liked = auction in current_user.auction_likes

        if plan:
            result = {
            "id":auction.id,
            "liked":liked,
            "item_id":auction.item.id,
            "title":auction.title,
            "ratio":auction.ratio,
            "description":auction.description,
            "product_description":auction.item.product.description,
            "images":auction.item.images,
            "max_members":auction.max_members,
            "base_price":int(auction.base_price),
            "max_price":int(auction.max_price),
            "main_price":int(auction.item.price),
            "start_date":auction.start_date,
            "participants":auction_participants,
            "remained_time":remained_time,
            "max_offers":plan.max_offers
            }
        else:
            result = {
            "id":auction.id,
            "liked":liked,
            "item_id":auction.item.id,
            "title":auction.title,
            "ratio":auction.ratio,
            "description":auction.description,
            "product_description":auction.item.product.description,
            "images":auction.item.images,
            "max_members":auction.max_members,
            "max_price":str(auction.max_price),
            "base_price":str(auction.base_price),
            "main_price":str(auction.item.price),
            "start_date":auction.start_date,
            "participants":auction_participants,
            "remained_time":remained_time,
            "max_offers":0
            }
        return make_response(jsonify({"auction":result}),200)

class AuctionGetPlans(Resource):
    def get(self,aid):
        auction=Auction.query.get(aid)
        plans = auction.plans.order_by('price DESC')
        plan_schema = AuctionPlanSchema(many=True)
        payment_methods = PaymentMethod.query.filter(PaymentMethod.title!='بدون پرداخت').order_by('type')
        payment_method_schema = PaymentMethodSchema(many=True)
        return make_response(jsonify({"plans":plan_schema.dump(plans),"methods":payment_method_schema.dump(payment_methods)}),200)

class AuctionUsers(Resource):
    def get(self,aid):
        result = Offer.query.filter_by(auction_id=aid).order_by('offers.created_at').all()
        offers = []
        for offer in result:
            if offer.user_plan and offer.user_plan.user:
                offers.append({
                "pretty_name":offer.user_plan.user.first_name + " " + offer.user_plan.user.last_name if (offer.user_plan.user.first_name and offer.user_plan.user.last_name) else offer.user_plan.user.username ,
                "avatar":offer.user_plan.user.avatar,
                "user_id":offer.user_plan.user.id,
                "id":offer.id,
                "date":offer.created_at,
                "win":offer.win,
                "current_price":str(offer.total_price),
                "current_bids":offer.current_bids,
                })
        return make_response(jsonify(offers),200)

class AuctionWinners(Resource):
    def get(self,aid):
        auction = Auction.query.get(aid)
        result = Auction.query.filter(Auction.start_date < auction.start_date,Auction.item_id==auction.item.id).order_by('start_date DESC').all()
        users = []
        for item in result:
            if item.id != aid:
                offer = Offer.query.filter_by(auction_id=item.id,win=True).first()
                if (offer):
                    users.append({
                    "pretty_name":offer.user_plan.user.first_name + " " + offer.user_plan.user.last_name if (offer.user_plan.user.first_name and offer.user_plan.user.last_name) else offer.user_plan.user.username ,
                    "avatar":offer.user_plan.user.avatar,
                    "participants":item.participants.count(),
                    "main_price":str(item.item.price),
                    "price":str(offer.total_price),
                    "auction_id":item.id,
                    "user_id":offer.user_plan.user.id,
                    "date":offer.created_at,
                    "discount":str(item.item.price - offer.total_price)
                    })
        return make_response(jsonify(users),200)
