from project.database import db
from project.model import *
from definitions import BASE_BID_PRICE

from flask import current_app, url_for, redirect, render_template, request, abort , session
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
from definitions import AUCTION_START_PROGRESS,AUCTION_WINNER_POINT_FRACTION
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

@socketio.on_error()  # handles all namespaces without an explicit error handler
def another_error_handler(e):
    print(" ********** error accured in socketio ********** : ",e)
    app.logger.error(str(e))
    return 400


# auction methods

@socketio.on('connect')
def connect():
    print ("new user connected")
    return emit("connect" , {"message":"websocket connected"})

@socketio.on('mehdi')
def connect():
    print ("mehdi user connected")
    return emit("mehdi_connect" , {"message":"websocket connected"})

@socketio.on('keepalive')
def keepalive():
    return emit("keepalive" , "websocket keepalive")

@socketio.on('join_public')
def join(data):
    auction = Auction.query.get(data['auctionId'])
    if auction:
        room = data['auctionId']
        join_room(room)
        return emit("joined",{"message":"new client joined public_room","auctionId":auction.id},room=room)
    else:
        return emit("failed",{"error":{"message":"undefined auctionId","reason":"auctionId","status":401}},room=room)

@socketio.on('join_private')
@authenticated
def join(data,current_user):
    private_room = data['authorization']
    join_room(private_room)
    return emit("joined",{"message":"new client joined private_room","auctionId":data['auctionId']},room=private_room)

@socketio.on('leave')
@authenticated
def leave(data):
    room = data['auctionId']
    private_room = data['authorization']
    leave_room(room)
    leave_room(private_room)
    print ('leaving auction room',room)
    return emit("leaved", {"message": "client left room","auctionId":data['auctionId']}, room=room)

@socketio.on('getStatus')
def status(data):
    auction_room = data['auctionId']
    auction = Auction.query.get(data['auctionId'])
    if auction:
        status = {
            "bidPrice":0,
            "name":'بدون پیشنهاد',
            "avatar":''
            }
        last_bid = Bid.query.filter_by(auction_id=auction.id).order_by(Bid.created.desc()).first()
        if last_bid :
            status = {
                "bidPrice":str(last_bid.bid_price),
                "name":last_bid.user_plan.user.username,
                "avatar":last_bid.user_plan.user.avatar.image.split("'")[1],
                }
        return emit("status",{"status":status,"auctionId":data['auctionId']},room=auction_room)
    else:
        return emit("failed",{"message":SOCKET['AUCTION_NOT_FOUND'],"reason":"auction_not_found","status":400},room=auction_room)

@socketio.on('getUsers')
def users(data):
    auction_room = data["auctionId"]
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
                        "avatar" : bid.user_plan.user.avatar.image.split("'")[1],
                        "level":bid.user_plan.user.level.number,
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
        return emit("users",{"users":users,"auctionId":data["auctionId"]},room=auction_room)

@socketio.on('getAuction')
@authenticated
def getAuction(data,current_user):
    auction = Auction.query.get(data["auctionId"])
    auction_room = data["auctionId"]
    if not auction :
        return emit("failed",{"message":SOCKET['AUCTION_NOT_FOUND'],"reason":"auction_not_found","status":400})

    if not auction.is_active :
        message = AUCTION['NOT_ACTIVE'].replace('attribute',auction.title)
        return emit("failed",{"message":message,"reason":"auction_not_active","status":400})

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
    emit("users",participants,room=auction_room)

    liked = False
    participated = False
    bids = 0

    if current_user:
        liked = auction in current_user.auction_likes
        participated = auction in current_user.auctions

    if participated :
        user_auction_plan = AuctionPlan.query.join(UserPlan).filter(AuctionPlan.auction_id==auction.id,UserPlan.user_id==current_user.id).first()
        user_plan = UserPlan.query.join(AuctionPlan).filter(AuctionPlan.auction_id==auction.id,UserPlan.user_id==current_user.id).first()
        my_last_bid = Bid.query.join(UserPlan).filter(UserPlan.id==user_plan.id,Bid.auction_id==auction.id).order_by(desc(Bid.created)).first()
        if my_last_bid:
            bids = my_last_bid.current_bids
        else:
            bids = user_auction_plan.max_bids

    discount = math.ceil(( (auction.item.price - auction.max_price) / auction.item.price )*100)
    images = []
    for image in auction.item.images.split("'"):
        if len(image) > 5:
            images.append(image)

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

    extraBids = {}
    if auction.have_extra_gems:
        extraBids = {
            "bids":auction.extra_bids,
            "gems":auction.required_gems,
            "target":auction.target_bid,
        }

    result = {
        "charity":charity,
        "auctionId":auction.id,
        "images":images,
        "level":auction.level.number,
        "maxLevel":Level.query.count(),
        "likeCount":auction.likes.count(),
        "participants":participants,
        "liked":liked,
        "participated":participated,
        "bids":bids,
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
        "extraBids":extraBids
    }
    return emit("auction",{"auction":result,"auctionId":data["auctionId"]}, room=auction_room)

@socketio.on('bid')
@authenticated
def bid(data,current_user):
    public_room = data["auctionId"]
    private_room = data['authorization']
    auction_id = data['auctionId']
    auction = Auction.query.get(auction_id)

    if not auction :
        return emit('failed',{"error":{"message":AUCTION['NOT_FOUND'],"reason":"auctionNotFound","status":400,"auctionId":data["auctionId"]}},room=private_room)

    if not auction.is_active :
        message = AUCTION['NOT_ACTIVE'].replace('attribute',auction.title)
        return emit('failed',{"error":{"message":AUCTION['NOT_ACTIVE'],"reason":"auctionNotActive","status":400,"auctionId":data["auctionId"]}},room=private_room)

    deadline = datetime.now() - timedelta(milliseconds=1000)
    if(auction.start_date < deadline and auction.done==False):
        return emit('failed',{"error":{"message":SOCKET['AUCTION_SYNCRONIZATION'],"reason":"auctionFinished","status":400,"auctionId":data["auctionId"]}},room=private_room)

    if(auction.start_date < deadline and auction.done==True):
        return emit('failed',{"error":{"message":SOCKET['AUCTION_FINISHED'],"reason":"auctionFinished","status":400,"auctionId":data["auctionId"]}},room=private_room)

    user_plan = UserPlan.query.filter_by(user_id = current_user.id).join(AuctionPlan).filter_by(auction_id=auction_id).first()
    auc_part = UserAuctionParticipation.query.filter_by(auction_id=auction_id,user_id=current_user.id).first()

    if(not (user_plan and auc_part)):
        return emit('failed',{"error":{"message":SOCKET['NOT_PARTICIPATED'],"reason":"notParticipated","status":400,"auctionId":data["auctionId"]}},room=private_room)

    remained = auctionSecondsDeadline(auction.start_date)
    if(remained > 59):
        return emit('failed',{"error":{"message":SOCKET['AUCTION_START_DEADLINE'],"reason":"auctionStartDeadline","status":400,"auctionId":data["auctionId"]}},room=private_room)


    my_last_bid = Bid.query.join(UserPlan).filter(UserPlan.id==user_plan.id,Bid.auction_id==auction_id).order_by(desc(Bid.created)).first()
    last_bid = Bid.query.filter_by(auction_id=auction_id).order_by(desc(Bid.created)).first()


    if(last_bid and my_last_bid and my_last_bid.id==last_bid.id):
        return emit("failed", {"error":{"message":SOCKET['REAPETED_BID'], "reason":"reapetedBid","status":400,"auctionId":data["auctionId"]}},room=private_room)

    if(my_last_bid and my_last_bid.current_bids == 0):
        return emit("failed", {"error":{"message":SOCKET['BIDS_FENITTO'],"reason":"noBids","status":400,"auctionId":data["auctionId"]}},room=private_room)

    remained = auctionMillisecondsDeadline(auction.start_date)
    if(remained < 10000):
        auction.start_date = datetime.now() + timedelta(milliseconds=11000)
        db.session.add(auction)
        db.session.commit()
        remained = auctionMillisecondsDeadline(auction.start_date)
        emit("reset",{"heartbeat":remained,"auctionId":auction.id},room=public_room)

    current_bids = 0
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
            current_bids = my_last_bid.current_bids - 1
        else:
            return emit("failed", {"error":{"message":SOCKET['BIDS_FENITTO'],"reason":"noBids","status":400,"auctionId":data["auctionId"]}},room=private_room)
            # leave_auction(data)
    elif(last_bid):
        #get last_bid price for offer
        if( last_bid.bid_price < auction.max_price):
            bid.bid_price = last_bid.bid_price + (BASE_BID_PRICE * auction.ratio)
        else:
            bid.bid_price = auction.max_price
        current_bids = user_plan.auction_plan.max_bids - 1
    else:
        #starting price for first offer
        bid.bid_price = auction.base_price + (BASE_BID_PRICE * auction.ratio)
        current_bids = user_plan.auction_plan.max_bids - 1

    bid.current_bids = current_bids
    db.session.add(bid)
    db.session.commit()

    last_bid = Bid.query.filter_by(auction_id=auction.id).order_by(Bid.created.desc()).first()
    if last_bid :
        status = {
            "bidPrice":str(last_bid.bid_price),
            "name":last_bid.user_plan.user.username,
            "avatar":last_bid.user_plan.user.avatar.image.split("'")[1],
            }

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
                    "avatar" : bid.user_plan.user.avatar.image.split("'")[1],
                    "level":bid.user_plan.user.level.number,
                })
                temp.add(bid.user_plan_id)

    emit("users",{"users":users,"auctionId":data["auctionId"]},room=public_room)
    emit("bids",{"bids":current_bids,"auctionId":data["auctionId"]},room=private_room)
    return emit("status",{"status":status,"auctionId":data["auctionId"]},room=public_room)

# user methods

@socketio.on('joinUser')
@authenticated
def userJoin(data,current_user):
    room = data['authorization']
    join_room(room)
    return emit("userJoined",{"message":"new user joined",},room=room)

@socketio.on('leaveUser')
@authenticated
def userLeave(data,current_user):
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
        # "orderCount":Order.query.filter_by(user_id = current_user.id,status = OrderStatus.UNPAID).count(),
        "level":current_user.level.number,
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
        shipment_methods = []
        for method in ItemShipment.query.join(ShipmentMethod).filter(ItemShipment.item_id==order.item_id).order_by(ShipmentMethod.title.desc()):
            shipment_methods.append({
                "orderId":order.id,
                "methodId":method.shipment_method.id,
                "title":method.shipment_method.title,
                "price":str(method.price)
            })

        item_garanties = []
        for item_garanty in ItemGaranty.query.join(Garanty).filter(ItemGaranty.item_id==order.item_id).order_by(Garanty.title.desc()):
            item_garanties.append({
                "orderId":order.id,
                "garantyId":item_garanty.garanty.id,
                "title":item_garanty.garanty.title,
                "price":str(item_garanty.price)
            })

        orders.append({
            "orderId":order.id,
            "itemId":order.item.id,
            "price":str(order.total_cost),
            "discount":str(order.total_discount),
            "title":order.item.title,
            "type":order.discount_status,
            "image":order.item.images.split("'")[1],
            "order_details":{
                "shipment_methods":shipment_methods,
                "item_garanties":item_garanties
            }
        })
    return emit("carts",orders,room=room)

@socketio.on('userScores')
@authenticated
def userStatus(data,current_user):
    room = data['authorization']
    oldUsers = User.query.order_by(User.points.desc()).limit(10)
    row = 0
    last_point = 999999999999999
    users = []
    for user in oldUsers:
        if last_point > user.points:
            row += 1
            last_point = user.points

        users.append({
            "row":row,
            "id":user.id,
            "points":user.points,
            "name":user.username,
            "level":user.level.number,
            "avatar":user.avatar.image.split("'")[1],
        })
    return emit("userScores",users,room=room)

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

def auctions_states():
    print ('auctions states servise is working...')
    done = False
    while True:
        if not done:
            done = True
            now = datetime.now()
            nextTime = now + timedelta(seconds=180)
            beforeTime = now - timedelta(seconds=10)
            auctions = db.session.query(Auction).filter(Auction.start_date > beforeTime , Auction.start_date < nextTime , Auction.done == False).order_by(Auction.start_date.desc())
            for auction in auctions:
                print(auction.title)
                remained = auctionMillisecondsDeadline(auction.start_date)

                if(remained > 60000):
                    socketio.emit("iceAge",{"state":"iceAge","auctionId":auction.id,"heartbeat":remained},broadcast=True)
                elif(remained <= 60000 and remained > 10000):
                    socketio.emit("holliDay",{"state":"holliDay","auctionId":auction.id,"heartbeat":remained})
                elif(remained <= 10000 and remained > -1000):
                    socketio.emit("hotSpot",{"state":"hotSpot","auctionId":auction.id,"heartbeat":remained})
                elif(remained < -1000 and remained > -3000):
                    socketio.emit("zeroTime",{"state":"zeroTime","auctionId":auction.id,"message":SOCKET['ZERO']})
                else:
                    last_bid = db.session.query(Bid).filter(Bid.auction_id==auction.id).order_by(Bid.created.desc()).first()
                    if last_bid:
                        diff = secondDiff(auction.start_date,last_bid.created)
                        print(diff)
                        if(diff < 10):
                            current_auction = db.session.query(Auction).get(auction.id)
                            current_auction.start_date = now + timedelta(milliseconds=10000)
                            db.session.add(current_auction)
                            db.session.commit()
                            remained = auctionMillisecondsDeadline(auction.start_date)
                            print('Refresh auction time')
                            socketio.emit("reset",{"heartbeat":remained,"auction_id":auction.id})
                        else:
                            print('Auction done ...')
                            last_bid.won=True
                            last_bid.user_plan.user.points += last_bid.user_plan.user.level.points_per_win
                            current_auction = db.session.query(Auction).get(auction.id)
                            current_auction.done=True

                            last_order = Order.query.filter_by(user_id=last_bid.user_plan.user.id,item_id=current_auction.item.id,status=OrderStatus.UNPAID).first()
                            if last_order :
                                last_order.total_cost = current_auction.item.price
                                last_order.discount_status = OrderDiscountStatus.AUCTIONWINNER
                                last_order.total_discount = current_auction.item.price - last_bid.bid_price
                                last_order.total = 1
                                last_order.item = auction.item
                                last_order.status = OrderStatus.UNPAID
                                db.session.add(last_order)
                            else:
                                new_order = Order()
                                new_order.user = last_bid.user_plan.user
                                new_order.item = current_auction.item
                                new_order.total_cost = current_auction.item.price
                                new_order.status = OrderStatus.UNPAID
                                new_order.discount_status = OrderDiscountStatus.AUCTIONWINNER
                                new_order.total = 1
                                new_order.total_discount = current_auction.item.price - last_bid.bid_price
                                db.session.add(new_order)

                            db.session.add(last_bid)
                            db.session.add(current_auction)
                            db.session.commit()

                            winner = {
                                "auctionTitle":current_auction.title,
                                "auctionImage":current_auction.image.split("'")[1],
                                "level":last_bid.user_plan.user.level.number,
                                "name":last_bid.user_plan.user.username,
                                "avatar":last_bid.user_plan.user.avatar.image.split("'")[1],
                                "bidPrice":str(last_bid.bid_price),
                                }
                            socketio.emit("winner",{"winner":winner,"auctionId":current_auction.id})

                            db.session.remove()
                    else:
                        current_auction = db.session.query(Auction).get(auction.id)
                        current_auction.done = True
                        db.session.add(current_auction)
                        db.session.commit()
                        print('feniTto for:',auction.id)
                        socketio.emit("feniTto",{"auctionId":auction.id,"error":{"message":SOCKET['FENITTO']}})

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
        if user.level:
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
            socketio.sleep(60)
            newUsers = db.session.query(User).order_by(User.points.desc()).limit(10)
            row = 0
            last_point = 999999999999
            for user in newUsers:
                if last_point > user.points:
                    row += 1
                    last_point = user.points
                if user.level :
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
        done = False

def auction_event_handler():
    print ('auction event handler servise is working...')
    done = False
    while True:
        if not done:
            today = datetime.now() - timedelta(seconds=5)
            auctions = db.session.query(Auction).filter(Auction.start_date > datetime.now() , Auction.updated >= today , Auction.done == False).order_by(Auction.start_date.desc())
            for auction in auctions:
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

                socketio.emit("users",participants,broadcast=True)

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

                extraBids = {}
                if auction.have_extra_gems:
                    extraBids = {
                        "bids":auction.extra_bids,
                        "gems":auction.required_gems,
                        "target":auction.target_bid,
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
                    "extraBids":extraBids
                }
                socketio.emit("auction",result, broadcast=True)
            db.session.remove()
        socketio.sleep(4)
    done = False

def levels():
    done = True
    while True:
        print ('sync user levels...')
        if not done:
            done = True
            users = db.session.query(User).order_by(User.points.desc()).limit(10)
            for user in users:
                current_level = db.session.query(Level).filter(user.points >= Level.required_points).order_by(Level.required_points.desc()).first()
                print (current_level)
                user.level = current_level
                db.session.add(user)
            db.session.commit()
            db.session.remove()
        done = False
        socketio.sleep(60)


@socketio.on('getAuctionItem')
@authenticated
def getAuctionItem(data,current_user):
    auction = Auction.query.get(data["auctionId"])
    auction_room = data["auctionId"]
    if not auction :
        return emit("failed",{"message":SOCKET['AUCTION_NOT_FOUND'],"reason":"auction_not_found","status":400})

    if not auction.is_active :
        message = AUCTION['NOT_ACTIVE'].replace('attribute',auction.title)
        return emit("failed",{"message":message,"reason":"auction_not_active","status":400})

    charity = {}
    if auction.charity:
        charity ={
            "icon":auction.charity.icon.split("'")[1],
            "description":auction.charity.description
        }

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
    bids = 0
    if current_user:
        liked = auction in current_user.auction_likes
        participated = auction in current_user.auctions

    if participated :
        user_auction_plan = AuctionPlan.query.join(UserPlan).filter(AuctionPlan.auction_id==auction.id,UserPlan.user_id==current_user.id).first()
        user_plan = UserPlan.query.join(AuctionPlan).filter(AuctionPlan.auction_id==auction.id,UserPlan.user_id==current_user.id).first()
        my_last_bid = Bid.query.join(UserPlan).filter(UserPlan.id==user_plan.id,Bid.auction_id==auction.id).order_by(desc(Bid.created)).first()
        if my_last_bid:
            bids = my_last_bid.current_bids
        else:
            bids = user_auction_plan.max_bids

    discount = math.ceil(( (auction.item.price - auction.max_price) / auction.item.price )*100)
    image = None
    if auction.advertisement:
        image = auction.advertisement.image.split("'")[1]
    else:
        image = auction.item.images.split("'")[1],

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
        "image":image,
        "level":auction.level.number,
        "maxLevel":Level.query.count(),
        "likeCount":auction.likes.count(),
        "participants":participants,
        "maxMembers":auction.max_members,
        "liked":liked,
        "participated":participated,
        "bids":bids,
        "tag":auction.tag,
        "title":auction.title,
        "basePrice":str(auction.base_price),
        "maxPrice":str(auction.max_price),
        "remainedTime":remainedTime,
        "discount":discount,
        "product":product,
        "status":status,
        "done":auction.done
    }

    return emit("auctionItem",{"auction":result,"auctionId":data["auctionId"]}, room=auction_room)

socketio.start_background_task(auctions_states)
socketio.start_background_task(scores)
socketio.start_background_task(levels)
# socketio.start_background_task(auction_event_handler)
