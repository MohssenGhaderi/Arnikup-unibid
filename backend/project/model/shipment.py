
import random
from project.database import db, Base
import datetime
import time

class ShipmentStatus:
    ORDERED = 'سفارش داده شده'
    IN_STORE = 'در انبار'
    READY_TO_SEND = 'آماده ارسال'
    SENT = 'ارسال شده'
    DELIVERED = 'تحویل داده شده'


class Shipment(Base):
    __tablename__ = 'shipments'
    id = db.Column(db.BigInteger, primary_key=True)
    guid = db.Column(db.String(64), default = random.randint(100000000000,10000000000000000))

    shipment_item_id = db.Column(db.BigInteger,db.ForeignKey('item_shipments.id'))
    shipment_item = db.relationship('ItemShipment')

    insurance_id = db.Column(db.BigInteger, db.ForeignKey('insurances.id'), nullable=True)
    insurance = db.relationship('Insurance')

    send_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)
    recieve_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now)

    status = db.Column(db.String(64),default=ShipmentStatus.ORDERED)

    order_id = db.Column(db.BigInteger, db.ForeignKey('orders.id'))
    order = db.relationship('Order')
    # payment = db.relationship('Payment')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        if(self.status):
            status = "ارسال موفقیت آمیز"
        else:
            status = "عدم ارسال موفقیت آمیز"
        return "روش ارسال :" + str(self.shipment_method) + " - تاریخ :" + str(self.send_date) + " - هزینه ارسال :" + str(self.shipment_method.price) + " - وضعیت :" + status

    def __init__(sefl):
        random.seed(datetime.now())
        self.guid = random.randint(100000000000,10000000000000000)
