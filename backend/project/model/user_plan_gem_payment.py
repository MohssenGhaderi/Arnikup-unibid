

from project import db
import datetime

class UserPlanGemPayment(db.Model):
    __tablename__ = 'user_plan_gem_payments'
    id = db.Column(db.BigInteger,primary_key=True)

    user_plan_id = db.Column(db.BigInteger,db.ForeignKey('user_plans.id'))
    user_plan = db.relationship('UserPlan')

    gem_payment_id = db.Column(db.BigInteger,db.ForeignKey('gem_payments.id'))
    gem_payment = db.relationship('GemPayment',cascade="all,delete",backref="user_plan_gem_payments")

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        if(self.gem_payment.user):
            return    "کاربر " + self.gem_payment.user.username + " "
