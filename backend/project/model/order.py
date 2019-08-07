
from project.database import db, Base
import datetime

# each order has a status for servicing
class OrderStatus:
    UNPAID = 'بدون پرداخت'
    PAYING = 'درحال پرداخت'
    DEACTIVATE = 'غیرفعال'
    PAID = 'پرداخت شده'

class OrderDiscountStatus:
    REGULAR = 'خرید محصول'
    INAUCTION = 'شرکت کننده حراجی'
    AUCTIONWINNER = 'برنده حراجی'
    EXPIRED = 'منقضی شده'

class Order(Base):
    __tablename__ = 'orders'
    id = db.Column(db.BigInteger, primary_key=True)

    description = db.Column(db.Text)

    status = db.Column(db.String(64),default=OrderStatus.UNPAID)
    discount_status = db.Column(db.String(64),default=OrderDiscountStatus.REGULAR)

    total = db.Column(db.Integer,nullable=False)

    total_cost = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    total_discount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')

    item_id = db.Column(db.BigInteger, db.ForeignKey('items.id'))
    item = db.relationship('Item')

    shipmet = db.relationship('Shipment')

    payment_id = db.Column(db.BigInteger,db.ForeignKey('payments.id'))
    payment = db.relationship('Payment',cascade="all,delete",backref="orders")

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return "کاربر : "+str(self.user) +" - محصول : "+ str(self.item) + " - تعداد : " + str(self.total)
