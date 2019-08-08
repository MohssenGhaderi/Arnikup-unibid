
from project import db
import datetime

class UserMessageStatus:
    UNREAD = "خوانده نشده"
    MARKASREAD = "خوانده شده"
    ANSWERED = "پاسخ داده شده"
    REJECTED = "رد شده"
    ACCEPTED = "پذیرفته شده"
    APPLYING = "در دست اقدام"
    EDITED = "ویرایش شده"

class UserMessage(db.Model):
    __tablename__ = 'user_messages'
    id = db.Column(db.BigInteger, primary_key=True)

    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    user = db.relationship('User')

    title = db.Column(db.String(128), nullable=False)

    subject = db.Column(db.String(128), nullable=False)

    status = db.Column(db.String(128), nullable=False, default=UserMessageStatus.UNREAD)

    message = db.Column(db.Text, nullable=False)

    answer = db.Column(db.Text, nullable=True)

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        try:
            return " ارسال توسط : " +  str(self.user.username) + " با عنوان : " + self.title + " درتاریخ : " + str(self.created)
        except Exception as e:
            return self.title
