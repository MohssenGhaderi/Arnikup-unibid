from project import db
import datetime

class UserAuctionParticipation(db.Model):
    __tablename__ = 'user_auction_participations'

    id = db.Column(db.BigInteger,primary_key=True)

    auction_id = db.Column(db.BigInteger,db.ForeignKey('auctions.id'))
    auction = db.relationship('Auction')

    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
