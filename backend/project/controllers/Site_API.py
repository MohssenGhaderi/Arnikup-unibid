from flask_restful import Resource, reqparse
from ..model import *
from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session, flash
import json
from project import app
from datetime import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
import os
from sqlalchemy import or_

from ..model.guest_message import GuestMessage
from definitions import MAX_SEARCH_RESULT


class SiteStates(Resource):
    def get(self):
        states = State.query.order_by('title').distinct().all()
        state_schema = StateSchema(many=True)
        return make_response(jsonify(state_schema.dump(states)),200)

class SiteSearchFilters(Resource):
    def get(self,order_by_price,order_by,total,keyword):
        now = datetime.now()
        result = None
        if order_by_price=="price":
            result = Auction.query.filter(or_(Auction.title.like("%"+keyword+"%"),Auction.description.like("%"+keyword+"%"))).join(Item).order_by("price " + order_by).limit(total)
        else:
            result = Auction.query.filter(or_(Auction.title.like("%"+keyword+"%"),Auction.description.like("%"+keyword+"%"))).order_by("start_date " + order_by).limit(total)

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

class SiteSearchAuctions(Resource):
    def get(self,keyword):
        result = Auction.query.filter(or_(Auction.title.like("%"+keyword+"%"),Auction.description.like("%"+keyword+"%"))).limit(MAX_SEARCH_RESULT)
        auctions = []
        for auction in result:
            auctions.append({
            "id":auction.id,
            "title":auction.title,
            "images":auction.item.images,
            "base_price":str(auction.base_price),
            })

        return make_response(jsonify(auctions),200)


        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteSearchAuctionsCategory(Resource):
    def get(self,cid,keyword):
        auctions = Auction.query.filter(or_(Auction.title.like("%"+keyword+"%"),Auction.description.like("%"+keyword+"%"))).join(Item).join(Product).join(Category).filter_by(id = cid)
        auctions = []
        for auction in result:
            auctions.append({
            "id":auction.id,
            "title":auction.title,
            "images":auction.item.images,
            "base_price":str(auction.base_price),
            })

        return make_response(jsonify(auctions),200)

class SiteCategoryMenuItems(Resource):
    def get(self):
        categories = []
        result = Category.query.all()
        for category in result:
            categories.append({
            "id":category.id,
            "title":category.title,
            "icon":category.icon
            })
        return make_response(jsonify(categories),200)

class SiteCategoryAuctions(Resource):
    def get(self,cid):
        now = datetime.now()
        result = Auction.query.filter(Auction.start_date >= now).join(Item).join(Product).join(Category).filter_by(id = cid)
        auctions=[]
        for a in result:
            auction = Auction.query.get(a.id)
            auction.remained_time = (auction.start_date - now).days * 24 * 60 * 60 + (auction.start_date - now).seconds
            auctions.append(auction)
        category = Category.query.get(cid)
        auction_schema = AuctionSchema(many=True)
        category_schema = CategorySchema()
        result ={'category':category_schema.dump(category),'auctions':auction_schema.dump(auctions)}
        return make_response(jsonify(result),200)

class SiteCategoryForAuctions(Resource):
    def get(self):
        now = datetime.now()
        categories = Category.query.all()
        result = []
        for category in categories:
            auction_schema = AuctionSchema(many=True)
            auctions = Auction.query.filter(Auction.start_date >= now).join(Item).join(Product).join(Category).filter_by(id = category.id).order_by("start_date DESC").all()
            auction_result =[]
            if(auctions):
                for auction in auctions:
                    auction_participants = []
                    for participant in auction.participants:
                        auction_participants.append({"id":participant.id,"username":participant.username})
                    remained_time = (auction.start_date - now).days * 24 * 60 * 60 + (auction.start_date - now).seconds
                    title = auction.title
                    if (len(auction.title) > 25):
                        title = auction.title[:25]+"..."

                    auction_result.append({
                    "id":auction.id,
                    "title":title,
                    "images":auction.item.images,
                    "base_price":str(auction.base_price),
                    "max_price":str(auction.max_price),
                    "remained_time":remained_time,
                    "participants":auction_participants,
                    "start_date":auction.start_date
                    })
                result.append({"title" : category.title,"icon":category.icon,"auctions":auction_result})
        return make_response(jsonify(result),200)

class SiteCategoryProducts(Resource):
    def get(self,cid):
        now = datetime.now()
        result = Auction.query.filter(Auction.start_date >= now).join(Item).order_by("price").join(Product).join(Category).filter_by(id = cid)
        auctions=[]
        for a in result:
            auction = Auction.query.get(a.id)
            auction.remained_time = (auction.start_date - now).seconds
            auction.left_from_created = (now.replace(hour=0,minute=0,second=0,microsecond=0) - now).seconds
            auctions.append(auction)
        category = Category.query.get(cid)
        auction_schema = AuctionSchema(many=True)
        category_schema = CategorySchema()
        result ={'category':category_schema.dump(category),'auctions':auction_schema.dump(auctions)}
        return make_response(jsonify(result),200)

class SiteCategoryProductFilters(Resource):
    def get(self,cid,order_by_price,order_by,total):
        now = datetime.now()
        result = None
        if order_by_price=="price":
            result = Auction.query.filter(Auction.start_date >= now).join(Item).order_by("price "+ order_by).join(Product).join(Category).filter_by(id = cid).limit(total)
        else:
            result = Auction.query.filter(Auction.start_date >= now).order_by("start_date "+ order_by).join(Item).join(Product).join(Category).filter_by(id = cid).limit(total)

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

        category = Category.query.get(cid)
        result ={'category':CategorySchema().dump(category),'auctions':auctions}
        return make_response(jsonify(result),200)

class SiteAuctionCarouselAds(Resource):
    def get(self):
        auctions = Auction.query.join(Advertisement).filter(Advertisement.show==True,Auction.start_date > datetime.now()).order_by("start_date DESC")
        result = []
        for auction in auctions:
            auction_participants = []
            for participant in auction.participants:
                auction_participants.append({"id":participant.id,"username":participant.username})
            result.append({
                "id":auction.id,
                "title":auction.advertisement.title,
                "description":auction.advertisement.description,
                "link":auction.advertisement.link,
                "link_title":auction.advertisement.link_title,
                "images":auction.advertisement.images,
                "discount":auction.advertisement.discount,
                "participants":auction_participants
            })
        return make_response(jsonify(result),200)

class SiteCategoryCarouselAds(Resource):
    def get(self,cid):
        now = datetime.now()
        auctions = Auction.query.filter(Auction.start_date >= now).join(Advertisement).filter(Advertisement.show==True).join(Item).join(Product).join(Category).filter_by(id = cid)
        auction_schema = AuctionSchema(many=True)
        return make_response(jsonify(auction_schema.dump(auctions)),200)

class SiteProductCarouselAds(Resource):
    def get(self):
        products = Product.query.join(Advertisement).filter(Advertisement.show==True)
        product_schema = ProductSchema(many=True)
        return make_response(jsonify(product_schema.dump(products)),200)

class SiteTodayEvents(Resource):
    def get(self):
        today = datetime.today()
        now = datetime.now()
        results = Event.query.filter_by(is_active = True).filter(Event.start_date <= today , Event.end_date >= today).all()
        events = []
        for event in results:
            days = (event.end_date - now).days
            events.append({
            "discount":event.discount,
            "description":event.description,
            "deadline":(days * 24 * 60 * 60) + (event.end_date - now).seconds
            })

        return make_response(jsonify(events),200)

class SiteTodayAuctions(Resource):
    def get(self):
        now = datetime.now()
        results = Auction.query.filter(Auction.start_date > now).order_by("start_date").limit(6)
        auctions=[]
        for auction in results:
            auction_participants = []
            for participant in auction.participants:
                auction_participants.append({"id":participant.id,"username":participant.username})
            days = (auction.start_date - now).days
            remained_time = (days * 24 * 60 * 60) + (auction.start_date - now).seconds

            auctions.append({
            "id":auction.id,
            "item_id":auction.item.id,
            "title":auction.title,
            "images":auction.item.images,
            "base_price":str(auction.base_price),
            "max_price":str(auction.max_price),
            "main_price":str(auction.item.price),
            "remained_time":remained_time,
            "participants":auction_participants,
            "max_members":auction.max_members,
            "start_date":auction.start_date,
            })
        return make_response(jsonify(auctions),200)

class SiteMostpopularAuctions(Resource):
    def get(self):
        today = datetime.today()
        now = datetime.now()
        res = db.session.query(Auction.id, db.func.count(user_auction_likes.c.user_id).label('total')).join(user_auction_likes).group_by(Auction.id).having(Auction.start_date >= today).order_by('total DESC').limit(10)
        ids = []
        for r in res:
            ids.append(r.id)

        result = db.session.query(Auction).filter(Auction.id.in_(ids)).order_by("start_date DESC").all()

        auctions =[]
        for auction in result:
            auction_participants = []
            for participant in auction.participants:
                auction_participants.append({"id":participant.id,"username":participant.username})
            remained_time = (auction.start_date - now).seconds
            auctions.append({
            "id":auction.id,
            "title":auction.title,
            "images":auction.item.images,
            "base_price":str(auction.base_price),
            "max_price":str(auction.max_price),
            "main_price":str(auction.item.price),
            "remained_time":remained_time,
            "participants":auction_participants,
            "max_members":auction.max_members,
            })
        return make_response(jsonify(auctions),200)

class SiteMostviewedAuctions(Resource):
    def get(self):
        today = datetime.today()
        now = datetime.now()
        res = db.session.query(Auction.id, db.func.count(user_auction_likes.c.user_id).label('total')).join(user_auction_views).group_by(Auction.id).having(Auction.start_date >= today).order_by('total DESC').limit(10)
        ids = []
        for r in res:
            ids.append(r.id)

        result = db.session.query(Auction).filter(Auction.id.in_(ids)).order_by("start_date DESC").all()

        auctions =[]
        for auction in result:
            auction_participants = []
            for participant in auction.participants:
                auction_participants.append({"id":participant.id,"username":participant.username})
            remained_time = (auction.start_date - now).seconds
            auctions.append({
            "id":auction.id,
            "title":auction.title,
            "images":auction.item.images,
            "base_price":str(auction.base_price),
            "max_price":str(auction.max_price),
            "main_price":str(auction.item.price),
            "remained_time":remained_time,
            "participants":auction_participants,
            "max_members":auction.max_members,
            })
        return make_response(jsonify(auctions),200)

class UserContactUs(Resource):

    def _allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in definitions.ALLOWED_EXTENTIONS

    @login_required
    def post(self):

        new_message = GuestMessage()

        new_message.full_name = request.get.json('full_name', None)
        new_message.email = request.get.json('email', None)
        new_message.message = request.get.json('message', None)
        new_message.website = request.get.json('website', None)

        db.session.add(new_message)
        db.session.commit()

        flash("پیام با موفقیت ارسال شد")

        return redirect(url_for('index'))

class SitePaymentMethods(Resource):

    def get(self):
        payment_methods = PaymentMethod.query.filter(PaymentMethod.title!='بدون پرداخت').order_by('type').all()
        payment_methods_schema = PaymentMethodSchema(many=True)
        return make_response(jsonify(payment_methods_schema.dump(payment_methods)), 200)

class SiteShipmentMethods(Resource):

    def get(self):
        shipment_methods = ShipmentMethod.query.order_by('price').all()
        shipment_methods_schema = ShipmentMethodSchema(many=True)
        return make_response(jsonify(shipment_methods_schema.dump(shipment_methods)), 200)
