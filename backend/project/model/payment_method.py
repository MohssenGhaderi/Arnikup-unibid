
from project.database import db, Base
import datetime

class Payment_Types:
    Credit = 0
    Online = 1
    CardToCard = 2
    BankReceipt = 3
    NOPAY = 4

class PaymentMethod(Base):
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
