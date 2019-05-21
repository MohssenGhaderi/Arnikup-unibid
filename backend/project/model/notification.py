
from project.database import db, Base
import datetime

class NotificationType:
    REGULAR = 1
    CHANGEPASS = 2038
    FORGOTPASS = 2021
    INVITOR = 2039
    SELFINVITATION = 2040

class Notification(Base):
    __tablename__ = 'notifications'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    sms = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(length=1024))
    details = db.Column(db.String(length=255))
    type = db.Column(db.Integer,nullable=False)
    users = db.relationship('User', secondary='user_notifications', back_populates='notifications',lazy='dynamic')
    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title
