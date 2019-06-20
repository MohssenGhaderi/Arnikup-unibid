from project.database import db
from project.model import *
from definitions import BASE_BID_PRICE

from flask import current_app, url_for, redirect, render_template, request, abort, make_response , jsonify , session
import json
from project import app, socketio, rj
from datetime import datetime , timedelta
import time
from flask_socketio import emit, join_room, leave_room
from flask_jwt_extended import jwt_required
from sqlalchemy import or_ , and_ , asc , desc
from project.lang.fa import *
import functools
import jwt
from rejson import Path
from project.helpers import *
import math
from definitions import AUCTION_START_PROGRESS
from threading import Thread


def authenticated(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        arguments = dict(*args)
        if 'authorization' in arguments:
            access_token = arguments['authorization'].strip()
            reason = 'unknown'
            message = TOKEN['unknown']
            current_user = None
            error = True
            try:
                token = jwt.decode(access_token, current_app.config['SECRET_KEY'])
                current_user = User.query.filter_by(username=token['uid']).first()
                error = False
                user_token = rj.jsonget(token['hash'], Path.rootPath())
                if not user_token:
                    reason = 'revoked'
                    message = TOKEN['revoked']
                    error = True

                if not current_user.is_verified:
                    reason = 'verified'
                    message = TOKEN['verified']
                    error = True


                if current_user.is_banned:
                    reason = 'banned'
                    message = TOKEN['banned']
                    error = True


                if not current_user.is_active:
                    reason = 'notActive'
                    message = TOKEN['notActive']
                    error = True

            except jwt.ExpiredSignatureError as e:
                reason = 'expired'
                message = TOKEN['expired']
                error = True

            except jwt.DecodeError as e:
                reason = 'decode'
                message = TOKEN['decode']
                error = True

            except jwt.InvalidTokenError as e:
                reason = 'issue'
                message = TOKEN['issue']
                error = True

            except jwt.exceptions.InvalidSignatureError as e:
                reason = 'malformed'
                message = TOKEN['malformed']
                error = True

            except:
                reason = 'unknown'
                message = TOKEN['unknown']

            if error:
                return emit("failed",{"error":{"message":message,"reason":reason,"status":401}})
            else:
                return f(*args, **kwargs,current_user=current_user)
        else:
            return emit("failed",{"error":{"message":TOKEN['required'],"reason":'tokenRequired',"status":401}}),
    return wrapped

# @socketio.on_error()  # handles all namespaces without an explicit error handler
# def another_error_handler(e):
#     print(e)
#     pass


# auction methods

@socketio.on('connect')
def connect():
    return emit("connect" , "websocket connected")

@socketio.on('join')
@authenticated
def join(data,current_user):
    auction = Auction.query.get(data['auctionId'])
    if auction:
        public_room = data['auctionId']
        private_room = data['authorization']
        join_room(public_room)
        join_room(private_room)
        return emit("joined",{"message":"new client joined",},room=public_room)
    else:
        return emit("failed",{"error":{"message":"undefined auctionId","reason":"auctionId","status":401}})

@socketio.on('leave')
def leave(data):
    room = data['auctionId']
    leave_room(room)
    print ('leaving auction room',room)
    return emit("leaved", {"message": "client left room"}, room=room)

@socketio.on('getStatus')
def status(data):
    auction = Auction.query.get(data['auctionId'])
    if auction:
        last_bid = Bid.query.filter_by(auction_id=auction.id).order_by(desc(Bid.created)).first()
        status = {
            "bidPrice":0,
            "name":'بدون پیشنهاد',
            "avatar":'',
            }
        if last_bid :
            status = {
                "bidPrice":str(last_bid.bid_price),
                "name":last_bid.user_plan.user.username,
                "avatar":last_bid.user_plan.user.avatar.image.split("'")[1],
                }
        return emit("status",status,broadcast=True)
    else:
        return emit("failed",{"message":SOCKET['AUCTION_NOT_FOUND'],"reason":"auction_not_found","status":400})

@socketio.on('getUsers')
def users(data):
    room = data["auctionId"]
    auction = Auction.query.get(data['auctionId'])
    if auction:
        result = Bid.query.filter_by(auction_id=auction.id).order_by(Bid.created.desc())
        users = []
        counter = 0
        temp = set()
        if result:
            for bid in result:
                if bid.user_plan_id not in temp:
                    counter += 1
                    users.append({
                        "row":counter,
                        "name" : bid.user_plan.user.username,
                        "bidPrice" : str(bid.bid_price),
                        "avatar" : bid.user_plan.user.avatar.image.split("'")[1]
                    })
                    temp.add(bid.user_plan_id)
        else:
            for participant in auction.participants:
                counter += 1
                users.append({
                    "row":counter,
                    "name" : participant.username,
                    "avatar" : participant.avatar.image.split("'")[1],
                    "level":participant.level.number,
                })


        return emit("users",users,broadcast=True)

@socketio.on('getAuction')
def getAuction(data):
    auction = Auction.query.get(data["auctionId"])
    if not auction :
        return make_response(jsonify({"success":False,"reason":'auctionId',"message":AUCTION['NOT_FOUND']}),400)

    if not auction.is_active :
        message = AUCTION['NOT_ACTIVE'].replace('attribute',auction.title)
        return make_response(jsonify({"success":False,"reason":'auctionDeactivated',"message":message}),403)

    charity = {}
    if auction.charity:
        charity ={
            "icon":auction.charity.icon.split("'")[1],
            "description":auction.charity.description
        }

    participants = []
    all_participants = auction.participants.order_by(desc(UserAuctionParticipation.created))
    counter = all_participants.count() + 1
    for participant in all_participants:
        counter -= 1
        participants.append({
            "row":counter,
            "name":participant.username,
            "avatar":participant.avatar.image.split("'")[1],
            "level":participant.level.number,
        })

    emit("users",participants,broadcast=True)

    discount = math.ceil(( (auction.item.price - auction.max_price) / auction.item.price )*100)
    images = []
    for image in auction.item.images.split("'"):
        if len(image) > 5:
            images.append(image)

    # images.append(auction.item.images.split("'")[1])

    product = {}
    if auction.item.quantity > 0:
        product = {
            "price":str(auction.item.price),
            "discount":str(auction.item.discount),
            "quantity":auction.item.quantity,
        }

    status = {}
    remainedTime = auctionMillisecondsDeadline(auction.start_date)
    last_bid = Bid.query.filter_by(auction_id=auction.id).order_by(desc(Bid.created)).first()
    if last_bid :
        status = {
            "bidPrice":str(last_bid.bid_price),
            "name":last_bid.user_plan.user.username,
            "avatar":last_bid.user_plan.user.avatar.image.split("'")[1],
            }

    result = {
        "charity":charity,
        "auctionId":auction.id,
        "images":images,
        "level":auction.level.number,
        "maxLevel":Level.query.count(),
        "likeCount":auction.likes.count(),
        "participants":participants,
        "maxMembers":auction.max_members,
        "tag":auction.tag,
        "title":auction.title,
        "basePrice":str(auction.base_price),
        "maxPrice":str(auction.max_price),
        "remainedTime":remainedTime,
        "discount":discount,
        "product":product,
        "status":status,
        "done":auction.done,
    }
    return emit("auction",result, broadcast=True)

@socketio.on('bid')
@authenticated
def bid(data,current_user):
    room = data["auctionId"]
    private = data['authorization']
    # try:
    auction_id = data['auctionId']
    auction = Auction.query.get(auction_id)

    if not auction :
        return emit('failed',{"error":{"message":AUCTION['NOT_FOUND'],"reason":"auctionNotFound","status":400}})

    if not auction.is_active :
        message = AUCTION['NOT_ACTIVE'].replace('attribute',auction.title)
        return emit('failed',{"error":{"message":AUCTION['NOT_ACTIVE'],"reason":"auctionNotActive","status":400}})

    deadline = datetime.now() - timedelta(milliseconds=1000)
    if(auction.start_date < deadline):
        return emit('failed',{"error":{"message":SOCKET['AUCTION_FINISHED'],"reason":"auctionFinished","status":400}})

    user_plan = UserPlan.query.filter_by(user_id = current_user.id).join(AuctionPlan).filter_by(auction_id=auction_id).first()
    auc_part = UserAuctionParticipation.query.filter_by(auction_id=auction_id,user_id=current_user.id).first()

    if(not (user_plan and auc_part)):
        return emit('failed',{"error":{"message":SOCKET['NOT_PARTICIPATED'],"reason":"notParticipated","status":400}})

    remained = auctionSecondsDeadline(auction.start_date)
    if(remained > 60):
        return emit('failed',{"error":{"message":SOCKET['AUCTION_START_DEADLINE'],"reason":"auctionStartDeadline","status":400}})


    my_last_bid = Bid.query.join(UserPlan).filter(UserPlan.id==user_plan.id,Bid.auction_id==auction_id).order_by(desc(Bid.created)).first()
    last_bid = Bid.query.filter_by(auction_id=auction_id).order_by(desc(Bid.created)).first()


    if(last_bid and my_last_bid and my_last_bid.id==last_bid.id):
        return emit("failed", {"error":{"message":SOCKET['REAPETED_BID'], "reason":"reapetedBid","status":400}})

    if(my_last_bid and my_last_bid.current_bids == 0):
        return emit("failed", {"error":{"message":SOCKET['BIDS_FENITTO'],"reason":"noBids","status":400}})

    remained = auctionMillisecondsDeadline(auction.start_date)
    if(remained < 10000):
        auction.start_date = datetime.now() + timedelta(milliseconds=11000)
        db.session.add(auction)
        db.session.commit()
        remained = auctionMillisecondsDeadline(auction.start_date)

    bid_count = Bid.query.filter_by(auction_id=auction_id).count() + 1
    bid = Bid()
    bid.user_plan = user_plan
    bid.auction = auction

    if(my_last_bid):
        if(my_last_bid.current_bids > 0):
            calculated_price = auction.base_price + bid_count * (BASE_BID_PRICE * auction.ratio)
            if( calculated_price < auction.max_price):
                bid.bid_price = calculated_price
            else:
                bid.bid_price = auction.max_price
            bid.current_bids = my_last_bid.current_bids - 1
        else:
            return emit("failed", {"error":{"message":SOCKET['BIDS_FENITTO'],"reason":"noBids","status":400}})
            # leave_auction(data)
    elif(last_bid):
        #get last_bid price for offer
        if( last_bid.bid_price < auction.max_price):
            bid.bid_price = last_bid.bid_price + (BASE_BID_PRICE * auction.ratio)
        else:
            bid.bid_price = auction.max_price
        bid.current_bids = user_plan.auction_plan.max_bids - 1
    else:
        #starting price for first offer
        bid.bid_price = auction.base_price + (BASE_BID_PRICE * auction.ratio)
        bid.current_bids = user_plan.auction_plan.max_bids - 1

    emit("remainBids",bid.current_bids,room=private)
    db.session.add(bid)
    db.session.commit()
    db.session.close()
    return emit("accepted",remained, broadcast=True)

# user methods

@socketio.on('joinUser')
@authenticated
def userJoin(data,current_user):
    room = data['authorization']
    join_room(room)
    return emit("userJoined",{"message":"new user joined",},room=room)

@socketio.on('leaveUser')
@authenticated
def userLeave(data):
    room = data['authorization']
    leave_room(room)
    print ('user leaving room',room)
    return emit("userLeaved", {"message": "user left room"}, room=room)

@socketio.on('userStatus')
@authenticated
def userStatus(data,current_user):
    room = data['authorization']
    result = []
    notifs = SiteNotification.query.filter_by(user_id=current_user.id).order_by(SiteNotification.created.desc())
    for notif in notifs:
        result.append({
        "id":notif.id,
        "title":notif.title,
        "text":notif.text,
        "seen":notif.seen,
        "link":notif.link,
        "date":str(notif.created),
        })

    notifs = UserNotification.query.filter_by(user_id=current_user.id).order_by(UserNotification.created.desc())
    for notif in notifs:
        result.append({
        "id":notif.notification.id,
        "title":notif.notification.title,
        "text":notif.notification.text,
        "seen":notif.seen,
        "link":notif.notification.link,
        "date":str(notif.notification.created),
        })

    notifs = UserAuctionNotification.query.filter_by(user_id=current_user.id).order_by(UserAuctionNotification.created.desc())
    for notif in notifs:
        result.append({
        "id":notif.auction_notification.id,
        "title":notif.auction_notification.title,
        "text":notif.auction_notification.text,
        "seen":notif.seen,
        "link":notif.auction_notification.link,
        "date":str(notif.auction_notification.created),
        })

    result = sorted(result, key=lambda r: r['date'],reverse=True)


    basics = {
        "coins":current_user.coins,
        "gems":current_user.gems,
        "avatar":current_user.avatar.image.split("'")[1],
        "orderCount":Order.query.filter_by(user_id = current_user.id,status = OrderStatus.UNPAID).count(),
        "notifications":result
    }

    return emit("userStatus",basics,room=room)

@socketio.on('userProfileStatus')
@authenticated
def userStatus(data,current_user):
    room = data['authorization']
    user = {
        "username":current_user.username,
        "fullName":current_user.full_name,
        "mobile":current_user.mobile,
        "email":current_user.email,
        "level":current_user.level.number,
        "maxLevel":Level.query.count(),
        "avatar":current_user.avatar.image.split("'")[1],
        "orderCount":Order.query.filter_by(user_id = current_user.id,status = OrderStatus.UNPAID).count(),
    }
    return emit("profileStatus",user,room=room)

@socketio.on('userCarts')
@authenticated
def userStatus(data,current_user):
    room = data['authorization']
    order_result = Order.query.filter_by(user_id = current_user.id,status = OrderStatus.UNPAID).order_by(Order.created.desc())
    orders = []
    for order in order_result:
        orders.append({
            "orderId":order.id,
            "itemId":order.item.id,
            "price":str(order.total_cost),
            "discount":str(order.total_discount),
            "title":order.item.title,
            "image":order.item.images.split("'")[1]
        })
    return emit("carts",orders,room=room)

@socketio.on('userScores')
@authenticated
def userStatus(data,current_user):
    room = data['authorization']
    order_result = Order.query.filter_by(user_id = current_user.id,status = OrderStatus.UNPAID).order_by(Order.created.desc())
    orders = []
    for order in order_result:
        orders.append({
            "orderId":order.id,
            "itemId":order.item.id,
            "price":str(order.total_cost),
            "discount":str(order.total_discount),
            "title":order.item.title,
            "image":order.item.images.split("'")[1]
        })
    return emit("carts",orders,room=room)

@socketio.on('getAvatars')
@authenticated
def getAvatars(data,current_user):
    room = data['authorization']
    avatar_result = Avatar.query.order_by(Avatar.created.desc(),Avatar.needed_gems.desc())
    avatars = []
    for avatar in avatar_result:
        free = True
        selected = False
        if avatar.needed_gems > 0:
            free = False
        if avatar.id == current_user.avatar.id:
            selected = True

        avatars.append({
            "image" : avatar.image.split("'")[1],
            "avatarId" : avatar.id,
            "title" : avatar.title,
            "free" : free,
            "selected" : selected,
            "gemsNeed" : avatar.needed_gems,
            "owned" : avatar in current_user.avatars
        })
    return emit("avatars",avatars,room=room)


# live long services
def auction_doner():
    print ('auction_doner is working...')
    done = False
    while True:
        if not done:
            done = True
            now = datetime.now()
            auctions = db.session.query(Auction).filter(Auction.start_date < now , Auction.done==False).order_by(Auction.start_date.desc())
            for auction in auctions:
                print(auction.start_date)
                last_bid = db.session.query(Bid).filter(Bid.auction_id==auction.id).order_by(Bid.created.desc()).first()
                if last_bid:
                    diff = secondDiff(auction.start_date,last_bid.created)
                    if(diff < 9):
                        remained = 10000
                        auction.start_date = now + timedelta(milliseconds=10000)
                        db.session.add(auction)
                        db.session.commit()
                        print ('auction_doner is working...')
                        print('Continue')
                        socketio.emit("remained",remained, broadcast=True)
                    else:
                        print ('auction_doner is working...')
                        print('Done')
                        last_bid.won=True
                        auction.done=True
                        db.session.add(last_bid)
                        db.session.add(auction)
                        db.session.commit()

                        winner = {
                            "level":last_bid.user_plan.user.level.number,
                            "name":last_bid.user_plan.user.username,
                            "avatar":last_bid.user_plan.user.avatar.image.split("'")[1],
                            "bidPrice":str(last_bid.bid_price),
                            }
                        socketio.emit("winner",winner,broadcast=True)

                        db.session.remove()
                else:
                    socketio.emit("done","auction done without bid", broadcast=True)

            db.session.remove()
        socketio.sleep(3)
        done = False

def auction_states():
    print ('auction states servise is working...')
    done = False
    while True:
        if not done:
            done = True
            today = datetime.now() - timedelta(seconds=3)
            tomorrow = datetime.now() + timedelta(days=1)
            # auctions = db.session.query(Auction.start_date).filter(Auction.start_date >= today , Auction.start_date < tomorrow , Auction.done == False).order_by(Auction.start_date.desc())
            auctions = db.session.query(Auction.start_date).filter(Auction.start_date >= today , Auction.done == False).order_by(Auction.start_date.desc())
            for auction in auctions:
                states = {
                    "iceAge":False,
                    "holliDay":False,
                    "hotSpot":False,
                    "feniTto":False,
                    "heartbeat":0
                }
                remained = auctionSecondsDeadline(auction.start_date)
                if(remained > 60):
                    states['iceAge'] = True
                elif(remained <= 60 and remained > 10):
                    states['holliDay'] = True
                elif(remained <= 10 and remained > -1):
                    states['hotSpot'] = True
                else:
                    states['feniTto'] = True
                states['heartbeat'] = remained

                socketio.emit("states",states, broadcast=True)
            db.session.remove()
        socketio.sleep(1)
        done = False

def scores():
    print ('scores servise is working...')
    done = False
    ousers = []
    oldUsers = db.session.query(User).order_by(User.points.desc()).limit(10)
    row = 0
    last_point = 999999999999999
    for user in oldUsers:

        if last_point > user.points:
            row += 1
            last_point = user.points

        ousers.append({
            "row":row,
            "id":user.id,
            "points":user.points,
            "name":user.username,
            "level":user.level.number,
            "avatar":user.avatar.image.split("'")[1],
        })
        last_point = user.points
    while True:
        nusers = []
        print ('sync user scores...')
        if not done:
            done = True
            socketio.sleep(30)
            newUsers = db.session.query(User).order_by(User.points.desc()).limit(10)
            row = 0
            last_point = 999999999999
            for user in newUsers:
                if last_point > user.points:
                    row += 1
                    last_point = user.points
                nusers.append({
                    "row":row,
                    "id":user.id,
                    "points":user.points,
                    "name":user.username,
                    "level":user.level.number,
                    "avatar":user.avatar.image.split("'")[1]
                })
            scores = []
            for ou in ousers:
                score = {}
                for nu in nusers:
                    if ou['id'] == nu['id']:
                        if nu['points'] > ou['points'] or nu['row'] < ou['row']:
                            score['status'] = "up"
                            break
                        elif nu['points'] < ou['points'] or nu['row'] > ou['row']:
                            score['status'] = "down"
                            break
                        else:
                            score['status'] = "equal"
                            break
                score['userId'] = ou['id']
                score['points'] = ou['points']
                score['row'] = ou['row']
                score['name'] = ou['name']
                score['level'] = ou['level']
                score['avatar'] = ou['avatar']
                scores.append(score)

            socketio.emit("scores",scores, broadcast=True)
            ousers = nusers

            db.session.remove()
        socketio.sleep(1)
        done = False

# def auction_states():
#     print ('user orders servise is working...')
#     done = False
#     while True:
#         if not done:
#             done = True
#             orders = db.session.query(User).join(Order).filter(Order.status==OrderStatus.UNPAID).order_by(Order.created.desc())
#             for auction in auctions:
#                 states = {
#                     "iceAge":False,
#                     "holliDay":False,
#                     "hotSpot":False,
#                     "feniTto":False,
#                     "heartbeat":0
#                 }
#                 remained = auctionSecondsDeadline(auction.start_date)
#                 if(remained > 60):
#                     states['iceAge'] = True
#                 elif(remained <= 60 and remained > 10):
#                     states['holliDay'] = True
#                 elif(remained <= 10 and remained > -1):
#                     states['hotSpot'] = True
#                 else:
#                     states['feniTto'] = True
#                 states['heartbeat'] = remained
#
#                 socketio.emit("states",states, broadcast=True)
#             db.session.remove()
#         socketio.sleep(1)
#         done = False

socketio.start_background_task(auction_doner)
socketio.start_background_task(auction_states)
socketio.start_background_task(scores)
# socketio.start_background_task(user_orders)

    # result = User.query.join(UserAuctionParticipation).join(UserPlan).join(Bid).filter_by(auction_id=auction_id).order_by(desc(Bid.created))
    # users = []
    # for user in result:
    #     user_plan = UserPlan.query.filter_by(user_id=user.id,auction_id=auction_id).first()
    #     user_last_bid = Offer.query.filter_by(user_plan_id=user_plan.id,auction_id=auction_id).order_by('created_at DESC').first()
    #     current_bids = user_last_bid.current_bids
    #     current_offer_price = user_last_bid.bid_price
    #     pretty_name = user.first_name + " " + user.last_name if (user.first_name and user.last_name) else user.username
    #     users.append({
    #         "current_bids" : current_bids,
    #         "current_offer_price" : int(current_offer_price),
    #         "pretty_name" : pretty_name ,
    #         "avatar" : user.avatar,
    #         "id": user.id
    #     })

# except Exception as e:
#     return emit("failed", {"success":False,"reason": e.message})


# @socketio.on('sync_timers_join')
# def sync_timers_join(data):
#     room = data['room']
#     join_room(room)
#     emit("sync_timers_join" , room=room)
#     return 200
#
# @socketio.on('sync_auction_join')
# def sync_auction_join(data):
#     room = data['room']
#     join_room(room)
#     emit("sync_auction_join" , room=room)
#     return 200
#
# @socketio.on('sync_carts')
# def sync_carts(data):
#     room = data['room']
#     if current_user.is_authenticated:
#         result = Order.query.filter(or_(Order.status==OrderStatus.UNPAID, Order.status==OrderStatus.PAYING)).filter_by(user_id=current_user.id).order_by('created_at DESC')
#         orders = []
#         for order in result:
#             title = order.item.product.title
#             if (len(title) > 20):
#                 title = title[:20]+"..."
#             item_title = order.item.title
#             if (len(item_title) > 50):
#                 item_title = item_title[:50]+"..."
#             product_title = order.item.product.title
#             if (len(product_title) > 50):
#                 product_title = product_title[:50]+"..."
#             fulltitle = product_title + " - " + item_title
#             discounted_price = 0
#
#             if order.discount_status == OrderDiscountStatus.REGULAR:
#                 discounted_price = order.item.discount * order.total
#
#             elif order.discount_status == OrderDiscountStatus.INAUCTION :
#                 auction = current_user.auctions.join(Item).filter_by(id = order.item.id).order_by('auctions.created_at DESC').first()
#                 if(auction):
#                     userplan = current_user.user_plans.join(Auction).filter_by(id=auction.id).first()
#                     auctionplan = AuctionPlan.query.filter_by(auction_id=auction.id).join(UserPlan).filter_by(id=userplan.id).first()
#                     if auctionplan:
#                         discounted_price = auctionplan.discount
#
#             elif order.discount_status == OrderDiscountStatus.AUCTIONWINNER:
#                 auction = current_user.auctions.join(Item).filter_by(id = order.item.id).order_by('auctions.created_at DESC').first()
#                 if(auction):
#                     offer = Offer.query.filter_by(auction_id=auction.id,win=True).first()
#                     if offer:
#                         discounted_price = order.item.price - offer.bid_price
#
#             orders.append({
#             "id" : order.id,
#             "item_id" : order.item.id,
#             "title" : title,
#             "item_title" : item_title,
#             "product_title" : product_title,
#             "fulltitle" : product_title + " - " + item_title,
#             "images" : order.item.images,
#             "main_price" : str(order.total * order.item.price),
#             "discounted_price" : str(order.total * order.item.price - discounted_price),
#             "quantity" : order.item.quantity,
#             "total" : order.total,
#             "status" : order.status,
#             "discount_status" : order.discount_status,
#             })
#
#         emit("sync_carts",{"orders":orders}, room=room)
#         return 200
#     else:
#         if "orders" in session:
#             emit("sync_carts", session['orders'] , room=room)
#         else:
#             emit("sync_carts",[] , room=room)
#     return 200
#
# @socketio.on('sync_timers')
# def sync_timers(data):
#     now = datetime.now()
#     room = data['room']
#     results = Auction.query.filter(Auction.start_date > datetime.now()).order_by("start_date").limit(6)
#     auctions=[]
#     for auction in results:
#         auction_participants = []
#         for participant in auction.participants:
#             auction_participants.append({"id":participant.id,"username":participant.username})
#         days = (auction.start_date - now).days
#         remained_time = (days * 24 * 60 * 60) + (auction.start_date - now).seconds
#
#         auctions.append({
#         "id":auction.id,
#         "title":auction.title,
#         "images":auction.item.images,
#         "base_price":str(auction.base_price),
#         "max_price":str(auction.max_price),
#         "main_price":str(auction.item.price),
#         "remained_time":remained_time,
#         "participants":auction_participants,
#         "max_members":auction.max_members,
#         'expired':now > auction.start_date,
#         })
#     emit("sync_timers",{"auctions": auctions} , room=room)
#     return 200
#
# @socketio.on('sync_notifications')
# def sync_notifications(data):
#     room = data['room']
#     result = []
#     if current_user.is_authenticated:
#         notifs = UserNotification.query.filter_by(user_id=current_user.id).order_by('created_at DESC').all()
#         for notif in notifs:
#             result.append({
#             "id":notif.notification.id,
#             "title":notif.notification.title,
#             "text":notif.notification.text,
#             "seen":notif.seen,
#             "link":notif.notification.link,
#             "date":str(notif.notification.created_at),
#             })
#
#         notifs = UserAuctionNotification.query.filter_by(user_id=current_user.id).order_by('created_at DESC').all()
#         for notif in notifs:
#             result.append({
#             "id":notif.auction_notification.id,
#             "title":notif.auction_notification.title,
#             "text":notif.auction_notification.text,
#             "seen":notif.seen,
#             "link":notif.auction_notification.link,
#             "date":str(notif.auction_notification.created_at),
#             })
#
#         notifs = SiteNotification.query.filter_by(user_id=current_user.id).order_by('created_at DESC').all()
#         for notif in notifs:
#             result.append({
#             "id":notif.id,
#             "title":notif.title,
#             "text":notif.text,
#             "seen":notif.seen,
#             "link":notif.link,
#             "date":str(notif.created_at),
#             })
#
#         result = sorted(result, key=lambda r: r['date'],reverse=True)
#
#     emit("sync_notifications",{"notifications": result} , room=room)
#     return 200
#
# @socketio.on('join')
# def join(data):
#     room = data['auction_id']
#     join_room(room)
#     emit("joined",{"message":"new client joined"},room=room)
#     return 200
#
# @socketio.on('leave_auction')
# def leave_auction(data):
#     room = data['auction_id']
#     sync = data['room']
#     emit("leave_auction", {"message": "client left room"}, room=room)
#     leave_room(sync)
#     leave_room(room)
#     print ('leaving auction room',room)
#     print ('leaving sync room',room)
#     return 200
#
# @socketio.on('loadview')
# def loadview(data):
#     try:
#         room = data['auction_id']
#         auction_id = data['auction_id']
#         # auction = Auction.query.get(auction_id)
#         last_bid = Offer.query.filter_by(auction_id=auction_id).order_by('offers.created_at DESC').first()
#         result = User.query.join(UserAuctionParticipation).join(UserPlan).join(Offer).filter_by(auction_id=auction_id).order_by('offers.created_at DESC')
#         users = []
#         for user in result:
#             user_plan = UserPlan.query.filter_by(user_id=user.id,auction_id=auction_id).first()
#             user_last_bid = Offer.query.filter_by(user_plan_id=user_plan.id,auction_id=auction_id).order_by('offers.created_at DESC').first()
#             current_bids = user_last_bid.current_bids
#             current_offer_price = user_last_bid.bid_price
#             pretty_name = user.first_name + " " + user.last_name if (user.first_name and user.last_name) else user.username
#             users.append({
#                 "current_bids" : current_bids,
#                 "current_offer_price" : int(current_offer_price),
#                 "pretty_name" : pretty_name ,
#                 "avatar" : user.avatar,
#                 "id": user.id,
#             })
#
#         if(last_bid):
#             now = datetime.now()
#             days = (last_bid.auction.start_date - now).days
#             sign = lambda x: (1, -1)[x < 0]
#             remained_time = sign(days) * (last_bid.auction.start_date - datetime.now()).seconds
#
#             emit("update_view", {"success":True,"remained_time":remained_time , "current_offer_price": str(last_bid.bid_price),"users": users},room=room)
#         else:
#             emit("update_view", {"success":True , "current_offer_price": 0,"users": users},room=room)
#
#     except Exception as e:
#         emit("failed", {"reason": e.message})
#
#     return 200
#
# #authenticated users only

# def auction_done(data):
#     room = data["auction_id"]
#     auction_id = data['auction_id']
#     auction = Auction.query.get(auction_id)
#
#     # total_bids = Offer.query.filter_by(auction_id=auction_id).count()
#     last_bid = Offer.query.filter_by(auction_id=auction_id).order_by('offers.created_at DESC').first()
#
#     if(last_bid):
#         discounted_price = auction.item.price - last_bid.bid_price
#         if (not last_bid.win):
#             last_bid.win = True
#             db.session.add(last_bid)
#             db.session.commit()
#
#             winner = {
#             "username" : last_bid.user_plan.user.username,
#             "first_name" : last_bid.user_plan.user.first_name,
#             "last_name" : last_bid.user_plan.user.last_name,
#             "avatar" : last_bid.user_plan.user.avatar,
#             "discount" : int(auction.item.price - last_bid.bid_price)
#             }
#             #set the order for winner in he/she's carts
#
#             last_order = Order.query.filter_by(user_id=last_bid.user_plan.user.id,item_id=auction.item.id).first()
#
#             if last_order :
#                 last_order.total_cost = last_bid.bid_price
#                 last_order.discount_status = OrderDiscountStatus.AUCTIONWINNER
#                 last_order.total_discount = discounted_price
#                 last_order.total = 1
#                 db.session.add(last_order)
#                 db.session.commit()
#             else:
#                 new_order = Order()
#                 new_order.user = last_bid.user_plan.user
#                 new_order.item = auction.item
#                 new_order.total_cost = last_bid.bid_price
#                 new_order.status = OrderStatus.UNPAID
#                 new_order.discount_status = OrderDiscountStatus.AUCTIONWINNER
#                 new_order.total = 1
#                 new_order.total_discount = discounted_price
#                 db.session.add(new_order)
#                 db.session.commit()
#
#             emit("auction_done", {"success":True,"reason":"این حراجی به اتمام رسیده است", "winner": winner},room=room)
#             return 200
#         else:
#             winner = {
#             "username" : last_bid.user_plan.user.username,
#             "first_name" : last_bid.user_plan.user.first_name,
#             "last_name" : last_bid.user_plan.user.last_name,
#             "avatar" : last_bid.user_plan.user.avatar,
#             "discount" : int(discounted_price),
#             }
#             emit("auction_done", {"success":True,"reason":"این حراجی به اتمام رسیده است", "winner": winner},room=room)
#             return 200
#     else:
#         emit("auction_done", {"success":False, "reason":"این حراجی بدون پیشنهاد دهنده به پایان رسیده است"},room=room)
#         return 400
#
# def get_winner(data):
#     room = data["auction_id"]
#     auction_id = data['auction_id']
#     auction = Auction.query.get(auction_id)
#     win_offer = Offer.query.filter_by(auction_id=auction_id,win=True).order_by('offers.created_at DESC').first()
#     winner = {
#     "username" : win_offer.user_plan.user.username,
#     "first_name" : win_offer.user_plan.user.first_name,
#     "last_name" : win_offer.user_plan.user.last_name,
#     "avatar" : win_offer.user_plan.user.avatar,
#     "discount" : int(auction.item.price - win_offer.bid_price),
#     }
#     emit("auction_done", {"success":True,"reason":"این حراجی به اتمام رسیده است", "winner": winner },room=room)
#     return 200
#
# @socketio.on('get_remain_time')
# def get_remain_time(data):
#     room = data["auction_id"]
#     auction_id = data['auction_id']
#     auction = Auction.query.get(auction_id)
#     now = datetime.now()
#     days = (auction.start_date - now).days
#     sign = lambda x: (1, -1)[x < 0]
#     millisecond = (auction.start_date - now).seconds * 1000
#     remained = sign(days) * millisecond
#
#     # if(remained <= 0):
#     #     time.sleep(1)
#     #     auction = Auction.query.get(auction_id)
#     #     if(auction.start_date < datetime.now()):
#     #         print 'done from sync'
#     #         return auction_done(data)
#
#     # if(remained <= 0 and auction.start_date > datetime.now()):
#     #     print 'remained',remained
#     #     print 'inconsistency'
#     #     emit("remaining_time", 10200,room=room)
#
#     if(remained <= 0 and auction.start_date < datetime.now()):
#         print ('done from sync')
#         return auction_done(data)
#
#     emit("remaining_time", remained,room=room)
#     return 200
#
# @socketio.on('keepAlive')
# def keepAlive(data):
#     room = data['room']
#     emit("alive",room=room)
#     return 200
