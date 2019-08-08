

from project import db
import datetime

class UserPlanPayment(db.Model):
    __tablename__ = 'user_plan_payments'
    id = db.Column(db.BigInteger,primary_key=True)

    user_plan_id = db.Column(db.BigInteger,db.ForeignKey('user_plans.id'))
    user_plan = db.relationship('UserPlan')

    payment_id = db.Column(db.BigInteger,db.ForeignKey('payments.id'))
    payment = db.relationship('Payment')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        if(self.user):
            return    " پلن : " + self.user_plan.auction_plan.plan.title +" "+ self.user_plan.auction_plan.auction.title +" "+ self.user_plan.user.username + " "
