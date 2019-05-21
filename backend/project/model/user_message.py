
from project.database import db, Base
import datetime

class UserMessage(Base):
    __tablename__ = 'user_messages'
    id = db.Column(db.BigInteger, primary_key=True)

    user_id = db.Column(db.BigInteger, db.ForeignKey("users.id"))
    user = db.relationship('User')

    message = db.Column(db.String(1024), nullable=True)

    title = db.Column(db.String(128), nullable=True)

    subject = db.Column(db.String(512), nullable=False)

    file = db.Column(db.String(1024), nullable=True)

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        try:
            return " ارسال توسط : " +  str(self.user.username) + " با عنوان : " + self.title + " درتاریخ : " + str(self.created)
        except Exception as e:
            return self.title
