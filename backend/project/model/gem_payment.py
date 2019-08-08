from project import db
from datetime import datetime
import time
import random

class GemPayStatus:
    WAIT = 'شکل گیری'
    GEM_WAIT = 'منتظر تایید الماس'
    GEM_PAID = 'پرداخت الماس موفق'
    FAIL = 'همراه با خطا'
    DONE = 'انجام شده'

class GemPayType:
    NOTITLE = 'اولیه'
    CONVERTGEM = 'تبدیل به سکه'
    BUYPLAN = 'تبدیل به پلن حراجی'
    AVATAR = 'تبدیل به آواتار'
    BID = 'تبدیل به بید اضافه'

class GemPayment(db.Model):
    __tablename__ = 'gem_payments'
    id = db.Column(db.Integer, primary_key=True)
    GUID = db.Column(db.String(64) ,default = 0)
    paid_gems = db.Column(db.Integer(),default=0,nullable=False)
    type = db.Column(db.String(64),default=GemPayType.NOTITLE)
    status = db.Column(db.String(64),default=GemPayStatus.WAIT)
    # sequence = db.Column(db.String(255), nullable=False,default=GemPayStatus.WAIT)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')

    created = db.Column(db.TIMESTAMP, default=datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.now, nullable=False ,onupdate=datetime.now)

    def __str__(self):
        return "پرداخت با الماس "+ str(self.GUID) + " باوضعیت  :" + str(self.status) + " در تاریخ : " + str(self.created)

    def __init__(self):
        random.seed(datetime.now())
        self.GUID = random.randint(100000000000,10000000000000000)
