
from project.database import db, Base
import datetime


class ShipmentMethod(Base):
    __tablename__ = 'shipment_methods'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    aggrigation = db.Column(db.Float,default=1.0)
    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)


    def __str__(self):
        return self.title
