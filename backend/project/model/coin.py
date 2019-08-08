
from project import db
import datetime

class CoinType:
    INCHEST = 'پیشنهادات روزانه'
    FORSALE = 'بسته های فروشی'

class Coin(db.Model):
    __tablename__ = 'coins'
    id = db.Column(db.BigInteger,primary_key=True)
    title = db.Column(db.String(length=255), nullable=False)
    description = db.Column(db.Text,nullable=False)
    type = db.Column(db.String(64),nullable=False,default=CoinType.FORSALE)
    quantity = db.Column(db.Integer(),default=0,nullable=False)
    price = db.Column(db.DECIMAL(precision=20, scale=4),default=0)

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return  self.title +" به تعداد "+ str(self.quantity) + " از نوع " + self.type
