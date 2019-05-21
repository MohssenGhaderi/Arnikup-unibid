
from project.database import db, Base
import datetime


class ShipmentMethod(Base):
    __tablename__ = 'shipment_methods'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.DECIMAL(precision=20, scale=4), default=0)

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)


    def __str__(self):
        return self.title + " با هزینه ارسال : " + str(self.price)