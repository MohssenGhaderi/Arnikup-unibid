
from project import db
import datetime

class NotificationType:
    REGULAR = 1
    WELCOME = 3079
    CHANGEPASS = 3076
    FORGOTPASS = 3078
    PARTICIPATE = 3082
    INVITORGIFT = 3080
    INVITORSELFGIFT = 3081
    STARTAUCTION = 2984
    ENDAUCTION_ALLUSER = 3083
    ENDAUCTION_WINNER = 3084

class Notification(db.Model):
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
