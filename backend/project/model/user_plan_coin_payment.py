

from project import db
import datetime

class UserPlanCoinPayment(db.Model):
    __tablename__ = 'user_plan_coin_payments'
    id = db.Column(db.BigInteger,primary_key=True)

    user_plan_id = db.Column(db.BigInteger,db.ForeignKey('user_plans.id'))
    user_plan = db.relationship('UserPlan')

    coin_payment_id = db.Column(db.BigInteger,db.ForeignKey('coin_payments.id'))
    coin_payment = db.relationship('CoinPayment',cascade="all,delete",backref="user_plan_coin_payments")

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        if(self.coin_payment.user):
            return    "کاربر " + self.coin_payment.user.username + " "
