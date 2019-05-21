from project.database import db, Base
import datetime

class Bid(Base):
    __tablename__ = 'bids'

    id = db.Column(db.BigInteger, primary_key=True)

    bid_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    current_bids = db.Column(db.Integer,nullable=False)
    won = db.Column(db.Boolean,default=False)

    user_plan_id = db.Column(db.BigInteger,db.ForeignKey('user_plans.id'))
    user_plan = db.relationship('UserPlan')

    auction_id = db.Column(db.BigInteger,db.ForeignKey('auctions.id'))
    auction = db.relationship('Auction')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
