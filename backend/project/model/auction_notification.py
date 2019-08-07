from project.database import db, Base
import datetime

class AuctionNotificationType:
    REGULAR = 1
    FINISH = 2156
    START = 2158
    PARTICIPATE = 2159

class AuctionNotification(Base):
    __tablename__ = 'auction_notifications'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    sms = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(length=1024))
    details = db.Column(db.String(length=255))
    type = db.Column(db.String(length=255))
    auction_id = db.Column(db.BigInteger,db.ForeignKey('auctions.id'),nullable=False)
    auction = db.relationship('Auction')
    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title
