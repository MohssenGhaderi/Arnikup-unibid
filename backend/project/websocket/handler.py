from project.database import db
from project.model import *
from definitions import BASE_BID_PRICE

from flask import url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app, socketio
from datetime import datetime , timedelta
from flask_login import LoginManager, UserMixin,login_required, login_user, logout_user ,current_user
import time
from flask_socketio import emit, join_room, leave_room
from flask_jwt_extended import jwt_required
from sqlalchemy import or_ , and_

# @socketio.on_error()  # handles all namespaces without an explicit error handler
# def another_error_handler(e):
#     print(e)
#     pass

@socketio.on('sync_carts_join')
def sync_carts_join(data):
    room = data['room']
    join_room(room)
    emit("sync_carts_join" , room=room)
    return 200

@socketio.on('sync_timers_join')
def sync_timers_join(data):
    room = data['room']
    join_room(room)
    emit("sync_timers_join" , room=room)
    return 200

@socketio.on('sync_auction_join')
def sync_auction_join(data):
    room = data['room']
    join_room(room)
    emit("sync_auction_join" , room=room)
    return 200

@socketio.on('sync_carts')
def sync_carts(data):
    room = data['room']
    if current_user.is_authenticated:
        result = Order.query.filter(or_(Order.status==OrderStatus.UNPAID, Order.status==OrderStatus.PAYING)).filter_by(user_id=current_user.id).order_by('created_at DESC')
        orders = []
        for order in result:
            title = order.item.product.title
            if (len(title) > 20):
                title = title[:20]+"..."
            item_title = order.item.title
            if (len(item_title) > 50):
                item_title = item_title[:50]+"..."
            product_title = order.item.product.title
            if (len(product_title) > 50):
                product_title = product_title[:50]+"..."
            fulltitle = product_title + " - " + item_title
            discounted_price = 0

            if order.discount_status == OrderDiscountStatus.REGULAR:
                discounted_price = order.item.discount * order.total

            elif order.discount_status == OrderDiscountStatus.INAUCTION :
                auction = current_user.auctions.join(Item).filter_by(id = order.item.id).order_by('auctions.created_at DESC').first()
                if(auction):
                    userplan = current_user.user_plans.join(Auction).filter_by(id=auction.id).first()
                    auctionplan = AuctionPlan.query.filter_by(auction_id=auction.id).join(UserPlan).filter_by(id=userplan.id).first()
                    if auctionplan:
                        discounted_price = auctionplan.discount

            elif order.discount_status == OrderDiscountStatus.AUCTIONWINNER:
                auction = current_user.auctions.join(Item).filter_by(id = order.item.id).order_by('auctions.created_at DESC').first()
                if(auction):
                    offer = Offer.query.filter_by(auction_id=auction.id,win=True).first()
                    if offer:
                        discounted_price = order.item.price - offer.total_price

            orders.append({
            "id" : order.id,
            "item_id" : order.item.id,
            "title" : title,
            "item_title" : item_title,
            "product_title" : product_title,
            "fulltitle" : product_title + " - " + item_title,
            "images" : order.item.images,
            "main_price" : str(order.total * order.item.price),
            "discounted_price" : str(order.total * order.item.price - discounted_price),
            "quantity" : order.item.quantity,
            "total" : order.total,
            "status" : order.status,
            "discount_status" : order.discount_status,
            })

        emit("sync_carts",{"orders":orders}, room=room)
        return 200
    else:
        if "orders" in session:
            emit("sync_carts", session['orders'] , room=room)
        else:
            emit("sync_carts",[] , room=room)
    return 200

@socketio.on('sync_timers')
def sync_timers(data):
    now = datetime.now()
    room = data['room']
    results = Auction.query.filter(Auction.start_date > datetime.now()).order_by("start_date").limit(6)
    auctions=[]
    for auction in results:
        auction_participants = []
        for participant in auction.participants:
            auction_participants.append({"id":participant.id,"username":participant.username})
        days = (auction.start_date - now).days
        remained_time = (days * 24 * 60 * 60) + (auction.start_date - now).seconds

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
        'expired':now > auction.start_date,
        })
    emit("sync_timers",{"auctions": auctions} , room=room)
    return 200

@socketio.on('sync_notifications')
def sync_notifications(data):
    room = data['room']
    result = []
    if current_user.is_authenticated:
        notifs = UserNotification.query.filter_by(user_id=current_user.id).order_by('created_at DESC').all()
        for notif in notifs:
            result.append({
            "id":notif.notification.id,
            "title":notif.notification.title,
            "text":notif.notification.text,
            "seen":notif.seen,
            "link":notif.notification.link,
            "date":str(notif.notification.created_at),
            })

        notifs = UserAuctionNotification.query.filter_by(user_id=current_user.id).order_by('created_at DESC').all()
        for notif in notifs:
            result.append({
            "id":notif.auction_notification.id,
            "title":notif.auction_notification.title,
            "text":notif.auction_notification.text,
            "seen":notif.seen,
            "link":notif.auction_notification.link,
            "date":str(notif.auction_notification.created_at),
            })

        notifs = SiteNotification.query.filter_by(user_id=current_user.id).order_by('created_at DESC').all()
        for notif in notifs:
            result.append({
            "id":notif.id,
            "title":notif.title,
            "text":notif.text,
            "seen":notif.seen,
            "link":notif.link,
            "date":str(notif.created_at),
            })

        result = sorted(result, key=lambda r: r['date'],reverse=True)

    emit("sync_notifications",{"notifications": result} , room=room)
    return 200

@socketio.on('join')
def join(data):
    room = data['auction_id']
    join_room(room)
    emit("joined",{"message":"new client joined"},room=room)
    return 200

@socketio.on('leave_auction')
def leave_auction(data):
    room = data['auction_id']
    sync = data['room']
    emit("leave_auction", {"message": "client left room"}, room=room)
    leave_room(sync)
    leave_room(room)
    print ('leaving auction room',room)
    print ('leaving sync room',room)
    return 200

@socketio.on('loadview')
def loadview(data):
    try:
        room = data['auction_id']
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
                "id": user.id,
            })

        if(last_offer):
            now = datetime.now()
            days = (last_offer.auction.start_date - now).days
            sign = lambda x: (1, -1)[x < 0]
            remained_time = sign(days) * (last_offer.auction.start_date - datetime.now()).seconds

            emit("update_view", {"success":True,"remained_time":remained_time , "current_offer_price": str(last_offer.total_price),"users": users},room=room)
        else:
            emit("update_view", {"success":True , "current_offer_price": 0,"users": users},room=room)

    except Exception as e:
        emit("failed", {"reason": e.message})

    return 200

#authenticated users only
@socketio.on('bid')
def bid(data):
    # client_time = data["timestamp"].replace('/','-')
    # server_time = datetime.now()
    # print server_time - datetime.strptime(client_time, '%Y-%m-%d %H:%M:%S')
    # return 'ok'

    room = data["auction_id"]
    if not current_user.is_authenticated:
        return emit('failed',{"success":False,"reason":"جلسه کاری شما منقضی شده است لطفا دوباره به سایت وارد شوید"})

    try:
        auction_id = data['auction_id']
        auction = Auction.query.get(auction_id)

        if(auction.start_date < datetime.now()):
            return emit('failed',{"success":False,"reason":"وقت شرکت در حراجی به اتمام رسیده است"})

        user_plan = UserPlan.query.filter_by(user_id = current_user.id).join(AuctionPlan).filter_by(auction_id=auction_id).first()
        auc_part = UserAuctionParticipation.query.filter_by(auction_id=auction_id,user_id=current_user.id).first()

        if(not (user_plan and auc_part)):
            return emit('failed',{"success":False,"reason":"شما در این حراجی شرکت نکرده اید و مجوز ارسال پیشنهاد ندارید"})

        # check for one minutes remained for starting auction
        last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('offers.created_at DESC').first()

        if(last_offer and last_offer.win):
            return get_winner(data)

        now = datetime.now()
        days = (auction.start_date - now).days
        remained = (days * 24 * 60 * 60) + (auction.start_date - now).seconds

        if(remained > 60):
            return emit('failed',{"success":False,"reason":"تا یک دقیقه به شروع حراجی امکان ارسال پیشنهاد وجود ندارد"})

        my_last_offer = Offer.query.join(UserPlan).filter_by(id=user_plan.id,auction_id=auction_id).order_by('offers.created_at DESC').first()

        if(last_offer and my_last_offer and my_last_offer.id==last_offer.id):
            return emit("failed", {"success":False, "reason":"امکان ارسال پیشنهاد روی پیشنهاد خود را ندارید"})

        if(my_last_offer and my_last_offer.current_bids == 0):
            return emit("failed", {"success":False,"reason":"پیشنهادات شما به پایان رسید"})

        now = datetime.now()
        days = (auction.start_date - now).days
        sign = lambda x: (1, -1)[x < 0]

        millisecond = (auction.start_date - now).seconds * 1000
        microsecond = (auction.start_date - now).microseconds
        remained = sign(days) * (millisecond + microsecond/1000)

        # if(remained <= 0 ):
        #     print 'done from handler'
        #     return auction_done(data)
        #
        # elif(remained < 10700 and remained >0):
        #     remained = 10700
        #     auction.start_date = datetime.now() + timedelta(milliseconds=10700)
        #     db.session.add(auction)
        #     db.session.commit()

        # if(remained <= 0 ):
        #     print 'done from handler'
        #     return auction_done(data)

        # if(remained < 10700):
        #     remained = 10700
        #     auction.start_date = datetime.now() + timedelta(milliseconds=10700)
        #     db.session.add(auction)
        #     db.session.commit()

        if(remained < 10200):
            remained = 10200
            auction.start_date = datetime.now() + timedelta(milliseconds=10200)
            db.session.add(auction)
            db.session.commit()


        offer_count = Offer.query.filter_by(auction_id=auction_id).count() + 1
        offer = Offer()
        offer.user_plan=user_plan
        offer.auction=auction

        if(my_last_offer):
            if(my_last_offer.current_bids > 0):
                calculated_price = auction.base_price + offer_count * (BASE_BID_PRICE * auction.ratio)
                if( calculated_price < auction.max_price):
                    offer.total_price = calculated_price
                else:
                    offer.total_price = auction.max_price
                offer.current_bids = my_last_offer.current_bids - 1
            else:
                return emit("failed", {"success":False,"reason":"پیشنهادات شما به پایان رسید"})
                # leave_auction(data)
        elif(last_offer):
            #get last_offer price for offer
            if( last_offer.total_price < auction.max_price):
                offer.total_price = last_offer.total_price + (BASE_BID_PRICE * auction.ratio)
            else:
                offer.total_price = auction.max_price
            offer.current_bids = user_plan.auction_plan.max_offers - 1
        else:
            #starting price for first offer
            offer.total_price = auction.base_price + (BASE_BID_PRICE * auction.ratio)
            offer.current_bids = user_plan.auction_plan.max_offers - 1

        db.session.add(offer)
        db.session.commit()

        result = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(auction_id=auction_id).order_by('offers.created_at DESC')
        users = []
        for user in result:
            user_plan = UserPlan.query.filter_by(user_id=user.id,auction_id=auction_id).first()
            user_last_offer = Offer.query.filter_by(user_plan_id=user_plan.id,auction_id=auction_id).order_by('created_at DESC').first()
            current_bids = user_last_offer.current_bids
            current_offer_price = user_last_offer.total_price
            pretty_name = user.first_name + " " + user.last_name if (user.first_name and user.last_name) else user.username
            users.append({
                "current_bids" : current_bids,
                "current_offer_price" : int(current_offer_price),
                "pretty_name" : pretty_name ,
                "avatar" : user.avatar,
                "id": user.id
            })
        db.session.close()
        return emit("accepted", {"success": True, "current_bids": offer.current_bids, "total_price": str(offer.total_price) ,"users":users,"remained_time":remained},room=room)

    except Exception as e:
        return emit("failed", {"success":False,"reason": e.message})

def auction_done(data):
    room = data["auction_id"]
    auction_id = data['auction_id']
    auction = Auction.query.get(auction_id)

    # total_bids = Offer.query.filter_by(auction_id=auction_id).count()
    last_offer = Offer.query.filter_by(auction_id=auction_id).order_by('offers.created_at DESC').first()

    if(last_offer):
        discounted_price = auction.item.price - last_offer.total_price
        if (not last_offer.win):
            last_offer.win = True
            db.session.add(last_offer)
            db.session.commit()

            winner = {
            "username" : last_offer.user_plan.user.username,
            "first_name" : last_offer.user_plan.user.first_name,
            "last_name" : last_offer.user_plan.user.last_name,
            "avatar" : last_offer.user_plan.user.avatar,
            "discount" : int(auction.item.price - last_offer.total_price)
            }
            #set the order for winner in he/she's carts

            last_order = Order.query.filter_by(user_id=last_offer.user_plan.user.id,item_id=auction.item.id).first()

            if last_order :
                last_order.total_cost = last_offer.total_price
                last_order.discount_status = OrderDiscountStatus.AUCTIONWINNER
                last_order.total_discount = discounted_price
                last_order.total = 1
                db.session.add(last_order)
                db.session.commit()
            else:
                new_order = Order()
                new_order.user = last_offer.user_plan.user
                new_order.item = auction.item
                new_order.total_cost = last_offer.total_price
                new_order.status = OrderStatus.UNPAID
                new_order.discount_status = OrderDiscountStatus.AUCTIONWINNER
                new_order.total = 1
                new_order.total_discount = discounted_price
                db.session.add(new_order)
                db.session.commit()

            emit("auction_done", {"success":True,"reason":"این حراجی به اتمام رسیده است", "winner": winner},room=room)
            return 200
        else:
            winner = {
            "username" : last_offer.user_plan.user.username,
            "first_name" : last_offer.user_plan.user.first_name,
            "last_name" : last_offer.user_plan.user.last_name,
            "avatar" : last_offer.user_plan.user.avatar,
            "discount" : int(discounted_price),
            }
            emit("auction_done", {"success":True,"reason":"این حراجی به اتمام رسیده است", "winner": winner},room=room)
            return 200
    else:
        emit("auction_done", {"success":False, "reason":"این حراجی بدون پیشنهاد دهنده به پایان رسیده است"},room=room)
        return 400

def get_winner(data):
    room = data["auction_id"]
    auction_id = data['auction_id']
    auction = Auction.query.get(auction_id)
    win_offer = Offer.query.filter_by(auction_id=auction_id,win=True).order_by('offers.created_at DESC').first()
    winner = {
    "username" : win_offer.user_plan.user.username,
    "first_name" : win_offer.user_plan.user.first_name,
    "last_name" : win_offer.user_plan.user.last_name,
    "avatar" : win_offer.user_plan.user.avatar,
    "discount" : int(auction.item.price - win_offer.total_price),
    }
    emit("auction_done", {"success":True,"reason":"این حراجی به اتمام رسیده است", "winner": winner },room=room)
    return 200

@socketio.on('get_remain_time')
def get_remain_time(data):
    room = data["auction_id"]
    auction_id = data['auction_id']
    auction = Auction.query.get(auction_id)
    now = datetime.now()
    days = (auction.start_date - now).days
    sign = lambda x: (1, -1)[x < 0]
    millisecond = (auction.start_date - now).seconds * 1000
    remained = sign(days) * millisecond

    # if(remained <= 0):
    #     time.sleep(1)
    #     auction = Auction.query.get(auction_id)
    #     if(auction.start_date < datetime.now()):
    #         print 'done from sync'
    #         return auction_done(data)

    # if(remained <= 0 and auction.start_date > datetime.now()):
    #     print 'remained',remained
    #     print 'inconsistency'
    #     emit("remaining_time", 10200,room=room)

    if(remained <= 0 and auction.start_date < datetime.now()):
        print ('done from sync')
        return auction_done(data)

    emit("remaining_time", remained,room=room)
    return 200

@socketio.on('keepAlive')
def keepAlive(data):
    room = data['room']
    emit("alive",room=room)
    return 200
