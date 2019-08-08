from project import db
import datetime


class Insurance(db.Model):
    __tablename__ = "insurances"
    id = db.Column(db.BigInteger, primary_key=True)
    company = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text,nullable=False)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)

    shipments = db.relationship('Shipment')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        return self.company
