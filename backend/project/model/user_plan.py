

from project import db
import datetime

class UserPlan(db.Model):
    __tablename__ = 'user_plans'
    id = db.Column(db.BigInteger,primary_key=True)
    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')

    auction_plan_id = db.Column(db.BigInteger,db.ForeignKey('auction_plans.id'))
    auction_plan = db.relationship('AuctionPlan')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        if(self.user and self.auction_plan.auction):
            return    " پلن : " + self.auction_plan.plan.title +" "+ self.auction_plan.auction.title +" "+ self.user.username + " "
        return self.auction_plan.plan.title
