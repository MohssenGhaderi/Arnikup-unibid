#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from project import app, socketio
from project.database import *
from project.admin import admin
import time
import datetime
from project.model import *
from definitions import MAX_SMS_RETRY,SITE_PREFIX
from project.melipayamak import SendMessage
# from project.cron import cron
# from project.cron import auction_reminder

def auction_reminder():
    while True:
        try:
            print ('auction_reminder')
            auctions = Auction.query.filter(Auction.start_date > datetime.datetime.now()).order_by("start_date").all()
            for auction in auctions:
                now = datetime.datetime.now()
                days = (auction.start_date - now).days
                remained = (days * 24 * 60 * 60) + (auction.start_date - now).seconds

                starter = 'شروع حراجی با کد' + str(auction.id) + '٬ با عنوان :' + auction.title
                if (remained <= 300):
                    print ('remained',remained,"start :",starter)
                    for current_user in auction.participants:
                        if not SiteNotification.query.filter_by(title=starter,user_id=current_user.id).first():
                            title = str(auction.title).replace('حراجی','')
                            message = str(current_user) + ' عزیز ٬'\
                            + '\n' + 'حراجی '+ title +' تا دقایقی دیگر آغاز خواهد شد.'\
                            + '\n' + 'موفق باشید.'\
                            + '\n' + 'یونی بید'\
                            + '\n' + 'www.unibid.ir'

                            auction_notification = SiteNotification()
                            auction_notification.title = starter
                            auction_notification.text = str(current_user) + ' عزیز ٬ تا دقایقی دیگر حراجی ' + title + ' آغاز خواهد شد.'
                            auction_notification.sms = message
                            auction_notification.link = SITE_PREFIX+'/view/auction/'+str(auction.id)
                            auction_notification.details = str(current_user)+";"+title
                            auction_notification.type = SiteNotificationType.STARTAUCTION
                            auction_notification.user = current_user
                            db.session.add(auction_notification)
                            db.session.commit()
        except Exception as e:
            print (str(e))
        socketio.sleep(30)

def auction_end_reminder():
    while True:
        try:
            print ('auction_end_reminder')
            now = datetime.datetime.now()
            auction = Auction.query.filter(Auction.start_date < now).order_by("start_date DESC").first()
            if auction:
                winner = Offer.query.filter_by(auction_id=auction.id,win=True).order_by('created_at DESC').first()
                days = (now - auction.start_date).days
                left = (days * 24 * 60 * 60) + (now - auction.start_date).seconds
                ender = 'پایان حراجی با کد' + str(auction.id) + '٬ با عنوان :' + auction.title

                if winner and left < 300:
                    for current_user in auction.participants:
                        if winner.user_plan.user.id != current_user.id :
                            if not SiteNotification.query.filter_by(title=ender,user_id=current_user.id).first():
                                title = str(auction.title).replace('حراجی','')
                                message = str(current_user) + 'عزیز ٬'\
                                + '\n' + 'حراجی '+ title +' به پایان رسید.'\
                                + '\n' + 'با آرزوی موفقیت برای شما در حراجی های بعدی'\
                                + '\n' + 'www.unibid.ir'

                                auction_notification = SiteNotification()
                                auction_notification.title = ender
                                auction_notification.text = str(current_user) +' عزیز٬ حراجی '+ title + 'به اتمام رسید.'
                                auction_notification.sms = message
                                auction_notification.link = SITE_PREFIX+'/view/auction/'+str(auction.id)
                                auction_notification.details = str(current_user)+";"+title+";"+str(winner.user_plan.user)
                                auction_notification.type = SiteNotificationType.ENDAUCTION_ALLUSER
                                auction_notification.user = current_user
                                db.session.add(auction_notification)
                                db.session.commit()
                        else:
                            if not SiteNotification.query.filter_by(title=ender,user_id=current_user.id).first():
                                title = str(auction.title).replace('حراجی','')
                                message = str(current_user) + 'عزیز ٬'\
                                + '\n' + 'با عرض تبریک به شما حراجی '+ title +' به پایان رسید.'\
                                + '\n' + 'www.unibid.ir'

                                winner_notification = SiteNotification()
                                winner_notification.title = ender
                                winner_notification.text = 'حراجی '+ title + 'به پایان رسید. شما برنده این حراجی شدید!'
                                winner_notification.sms = message
                                winner_notification.link = SITE_PREFIX+'/cart'
                                winner_notification.details = str(winner.user_plan.user)+";"+title
                                winner_notification.type = SiteNotificationType.ENDAUCTION_WINNER
                                winner_notification.user = winner.user_plan.user
                                db.session.add(winner_notification)
                                db.session.commit()
        except Exception as e:
            print (str(e))
        socketio.sleep(60)

def sms_sender():
    while True:
        try:
            print ('sms_sender')
            # always send sms to auction users
            # recipients = UserNotification.query.filter(UserNotification.delivered==False,UserNotification.retry < MAX_SMS_RETRY,UserNotification.send_sms==True).all()
            recipients = UserNotification.query.filter(UserNotification.delivered==False).all()
            for recipient in recipients:
                print ("notify to :",str(recipient.user),"title :",recipient.notification.title)
                sms_response = SendMessage(recipient.user,recipient.notification.title,recipient.notification.sms,recipient.notification.details,recipient.notification.type)
                recipient.delivered = True
                db.session.add(recipient)
                db.session.commit()

            # recipients = UserAuctionNotification.query.filter(UserAuctionNotification.delivered==False,UserAuctionNotification.retry < MAX_SMS_RETRY).all()
            recipients = UserAuctionNotification.query.filter(UserAuctionNotification.delivered==False).all()
            for recipient in recipients:
                print ("notify to :",str(recipient.user),"title :",recipient.auction_notification.title)
                auction = recipient.auction_notification.auction
                sms_response = SendMessage(recipient.user,recipient.auction_notification.title,recipient.auction_notification.sms,recipient.auction_notification.details,recipient.auction_notification.type)
                recipient.delivered = True
                db.session.add(recipient)
                db.session.commit()

            # site_notifications = SiteNotification.query.filter(SiteNotification.delivered==False,SiteNotification.retry < MAX_SMS_RETRY).all()
            site_notifications = SiteNotification.query.filter(SiteNotification.delivered==False).all()
            for notification in site_notifications:
                print ("site notify to :",str(notification.user),"title :",notification.title)
                sms_response = SendMessage(notification.user,notification.title,notification.sms,notification.details,notification.type)
                # notification.delivered = sms_response['success']
                notification.delivered = True
                notification.retry += 1
                db.session.add(notification)
                db.session.commit()

        except Exception as e:
            print str(e)
        socketio.sleep(10)

def notification_cleaner():
    while True:
        print ('notification_cleaner')
        try:
            UserAuctionNotification.query.filter_by(delivered=True,seen=True).delete()
            UserNotification.query.filter_by(delivered=True,seen=True).delete()
            SiteNotification.query.filter_by(delivered=True,seen=True).delete()
            db.session.commit()
        except Exception as e:
            print (str(e))
        socketio.sleep(86400)


socketio.start_background_task(auction_reminder)
socketio.start_background_task(auction_end_reminder)
socketio.start_background_task(sms_sender)
socketio.start_background_task(notification_cleaner)
