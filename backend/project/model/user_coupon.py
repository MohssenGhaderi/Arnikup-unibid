
from project.database import db, Base
import datetime

class UserCoupon(Base):
    __tablename__ = 'user_coupons'
    id = db.Column(db.BigInteger,primary_key=True)
    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')

    coupon_id = db.Column(db.BigInteger,db.ForeignKey('coupons.id'))
    coupon = db.relationship('Coupon')

    used = db.Column(db.Boolean,default=False)

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        if(self.user and self.gift):
            return " جایزه : " + self.coupon.title +" به کاربر :"+ str(self.user.username) +" اختصاص دارد "
