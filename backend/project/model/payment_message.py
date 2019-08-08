

from project import db
import datetime

class PaymentMessage(db.Model):
    __tablename__ = 'payment_messages'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    payments = db.relationship('Payment' , secondary = 'payment_message_payments', back_populates='messages')
    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title
