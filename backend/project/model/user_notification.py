

from project import db
import datetime

class UserNotification(db.Model):
    __tablename__ = 'user_notifications'
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'),nullable=False)
    user = db.relationship('User')

    notification_id = db.Column(db.BigInteger,db.ForeignKey('notifications.id'),nullable=False)
    notification = db.relationship('Notification')

    delivered = db.Column(db.Boolean,default=False)
    seen = db.Column(db.Boolean,default=False)
    send_sms = db.Column(db.Boolean,default=False)
    retry = db.Column(db.Integer,default=0)

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return str(self.notification) +" - "+ str(self.user)
