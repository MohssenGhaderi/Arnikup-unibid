
from project.database import db, Base
import datetime

class UserAuctionNotification(Base):
    __tablename__ = 'user_auction_notifications'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')

    auction_notification_id = db.Column(db.BigInteger,db.ForeignKey('auction_notifications.id'))
    auction_notification = db.relationship('AuctionNotification')

    details = db.Column(db.Text)
    delivered = db.Column(db.Boolean,default=False)
    seen = db.Column(db.Boolean,default=False)
    retry = db.Column(db.Integer,default=1)

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)


    def __str__(self):
        return str(self.notification) +" - "+ str(self.user)
