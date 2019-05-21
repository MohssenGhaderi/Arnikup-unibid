
from project.database import db, Base
from datetime import datetime
import time
import random

class CoinPayStatus:
    WAIT = 'شکل گیری'
    COIN_WAIT = 'درحال محاسبه سکه'
    COIN_PAID = 'کسر از حساب موفق'
    FAIL = 'همراه با خطا'
    DONE = 'انجام شده'

class CoinPayType:
    NOTITLE = 'اولیه'
    PLANCOIN = 'خرید پلن حراجی با موجودی سکه'
    GEMFRACTION = 'شارژ کسری حساب الماس'

class CoinPayment(Base):
    __tablename__ = 'coin_payments'
    id = db.Column(db.Integer, primary_key=True)
    GUID = db.Column(db.String(64),nullable=False)
    paid_coins = db.Column(db.Integer(),default=0,nullable=False)
    type = db.Column(db.String(64),default=CoinPayType.NOTITLE)
    status = db.Column(db.String(64),default=CoinPayStatus.WAIT)
    sequence = db.Column(db.String(255), nullable=False,default=CoinPayStatus.WAIT)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')

    created = db.Column(db.TIMESTAMP, default=datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.now, nullable=False ,onupdate=datetime.now)

    def __str__(self):
        return " پرداخت با سکه "+ str(self.GUID) + " باوضعیت  :" + str(self.status) + " در تاریخ : " + str(self.created)

    def __init__(self):
        random.seed(datetime.now())
        self.GUID = random.randint(100000000000,10000000000000000)
