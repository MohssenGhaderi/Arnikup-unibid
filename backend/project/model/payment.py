import random
from project.database import db, Base
from datetime import datetime
import time

class PaymentStatus:
    PAID = 'پرداخت موفق'
    RETRY = 'تلاش مجدد'
    BANK = 'درگاه بانک'
    PAYING = 'درحال پرداخت'
    ERROR = 'خطا در پرداخت'
    ABORT = 'پرداخت لغو شده'
    ARCHIVE = 'پرداخت بایگانی شده'
    UNPAID = 'پرداخت نشده'

class PaymentType:
    NOTITLE = 'اولیه'
    COIN = 'خرید مستقیم سکه حراجی'
    GEM = 'خرید بسته الماس'
    PRODUCT = 'خرید محصول'
    CHEST = 'خرید پکیج پیشنهادی'
    FREE = 'خرید رایگان'

class Payment(Base):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    GUID = db.Column(db.String(128) ,default = random.randint(100000000000,10000000000000000))
    reference_id = db.Column(db.String(255),default = random.randint(100000000000,10000000000000000))
    amount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    discount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    type = db.Column(db.String(64),default=PaymentType.NOTITLE)
    status = db.Column(db.String(64),default=PaymentStatus.UNPAID)
    sequence = db.Column(db.String(255),nullable=False,default=PaymentStatus.UNPAID)
    details = db.Column(db.Text)

    # payment_method_id = db.Column(db.BigInteger,db.ForeignKey('payment_methods.id'),nullable=False)
    # payment_method = db.relationship('PaymentMethod')
    # orders = db.relationship('Order' , secondary = 'payment_orders', back_populates='payments')

    # sale_order_id = db.Column(db.String(255))
    # sale_refrence_id = db.Column(db.String(255))

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')

    # shipment = db.relationship('Shipment')

    messages = db.relationship('PaymentMessage' , secondary = 'payment_message_payments', back_populates='payments')

    created = db.Column(db.TIMESTAMP, default=datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.now, nullable=False ,onupdate=datetime.now)

    def __str__(self):
        return " پرداخت به کد رهگیری : "+ str(self.GUID) + " باوضعیت  :" + str(self.status) + " در تاریخ : " + str(self.created)

    def __init__(self):
        random.seed(datetime.now())
        self.GUID = random.randint(100000000000,10000000000000000)
        self.reference_id = random.randint(10000000000,100000000000000000)
