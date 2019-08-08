
from project import db
import datetime

class GuestSendType:
    MOBILE = 'موبایل'
    EMAIL = 'ایمیل'

class GuestMessage(db.Model):
    __tablename__ = 'guest_messages'
    id = db.Column(db.BigInteger, primary_key=True)

    ip = db.Column(db.String(128), nullable=False)

    full_name = db.Column(db.String(128), nullable=False)

    email = db.Column(db.String(128), nullable=True)

    mobile = db.Column(db.String(128), nullable=True)

    send_type = db.Column(db.String(64), nullable=False,default=GuestSendType.MOBILE)

    message = db.Column(db.Text, nullable=False)

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)

    def __str__(self):
        return " ارسال توسط :" + str(self.full_name) + " درتاریخ " + self.created
