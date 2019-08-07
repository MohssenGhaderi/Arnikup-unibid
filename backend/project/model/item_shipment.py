from project.database import db, Base
import datetime

class ItemShipment(Base):
    __tablename__ = 'item_shipments'

    id = db.Column(db.BigInteger,primary_key=True)
    price = db.Column(db.DECIMAL(precision=20, scale=4),nullable=False)

    item_id = db.Column(db.BigInteger, db.ForeignKey('items.id'))
    item = db.relationship('Item',cascade="all,delete")

    shipment_method_id = db.Column(db.BigInteger, db.ForeignKey('shipment_methods.id'))
    shipment_method = db.relationship('ShipmentMethod',cascade="all,delete")

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        try:
            return "ارسال محصول " + self.item.title + " با روش " + self.shipment_method.title + "باهزینه " + self.price
        except Exception as e:
            return "بدون عنوان"
