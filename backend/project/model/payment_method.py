
from project import db
import datetime

class Payment_Types:
    Credit = 'اعتبار'
    Online = 'پرداخت آنلاین'
    CardToCard = 'کارت به کارت'
    BankReceipt = 'فیش بانکی'
    NOPAY = 'رایگان'

class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    type = db.Column(db.Integer, nullable=False)
    details = db.Column(db.Text)

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title
