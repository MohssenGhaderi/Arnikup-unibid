import gevent
from gevent import monkey
monkey.patch_all()
from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from project.model.auction import Auction
from project.model.bid import Bid
from project.helpers import *

def remove_session():
    db.session.remove()

def auction_end_reminder():
    done = False
    while True:
        print ('auction_end_reminder')
        if not done:
            done = True
            now = datetime.now()
            print(now)
            auctions = db.session.query(Auction).filter(Auction.start_date < now , Auction.done==False).order_by(Auction.start_date.desc())
            for auction in auctions:
                print(auction.start_date)
                last_bid = db.session.query(Bid).filter(Bid.auction_id==auction.id).order_by(Bid.created.desc()).first()
                if last_bid:
                    diff = secondDiff(auction.start_date,last_bid.created)
                    if(diff < 10):
                        print('remained',diff)
                        socketio.emit("remained",diff,broadcast=True)
            remove_session()
        socketio.sleep(1)
        done = False


print('starting cron job server...')
params = {
	 'pingInterval': 2000,
     'pingTimeout': 1000,
}
socketio = SocketIO(**params)
app = Flask(__name__)
app.config.from_pyfile('config.py')
socketio.init_app(app)
db = SQLAlchemy(app)
Base = db.Model
socketio.start_background_task(auction_end_reminder)
socketio.run(app)
