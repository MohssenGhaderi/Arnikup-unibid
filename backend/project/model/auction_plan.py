from project import db
import datetime

class AuctionPlan(db.Model):
    __tablename__ = 'auction_plans'

    id = db.Column(db.BigInteger,primary_key=True)
    needed_coins = db.Column(db.Integer(),default=0,nullable=False)
    max_bids = db.Column(db.Integer,nullable=False)
    discount = db.Column(db.DECIMAL(precision=20, scale=4),nullable=False)

    auction_id = db.Column(db.BigInteger, db.ForeignKey('auctions.id'))
    auction = db.relationship('Auction')

    plan_id = db.Column(db.BigInteger, db.ForeignKey('plans.id'))
    plan = db.relationship('Plan')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        try:
            return self.plan.title + " " + self.auction.title
        except Exception as e:
            return " بدون حراجی "
