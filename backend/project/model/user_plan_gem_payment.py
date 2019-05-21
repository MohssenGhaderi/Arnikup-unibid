

from project.database import db, Base
import datetime

class UserPlanGemPayment(Base):
    __tablename__ = 'user_plan_gem_payments'
    id = db.Column(db.BigInteger,primary_key=True)

    user_plan_id = db.Column(db.BigInteger,db.ForeignKey('user_plans.id'))
    user_plan = db.relationship('UserPlan')

    gem_payment_id = db.Column(db.BigInteger,db.ForeignKey('gem_payments.id'))
    gem_payment = db.relationship('GemPayment')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        if(self.user_plane):
            return    " پلن : " + self.user_plane.auction_plan.plan.title +" "+ self.user_plane.auction_plan.auction.title +" "+ self.user_plane.user.username + " "
