from project import db
import datetime

payment_message_payments = db.Table('payment_message_payments', db.Model.metadata,
    db.Column('payment_id', db.ForeignKey('payments.id')),
    db.Column('payment_message_id', db.ForeignKey('payment_messages.id'))
)
