
from project import db
import datetime

class UserSMS(db.Model):
    __tablename__ = 'short_messages'
    id = db.Column(db.BigInteger, primary_key=True)

    title = db.Column(db.String(length=100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'),nullable=False)
    user = db.relationship('User')

    status_code = db.Column(db.BigInteger,nullable=False,default=0)
    delivered = db.Column(db.Boolean,default=False)

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)


    def __str__(self):
        if(self.delivered):
            return self.title + " تحویل داده شده به کاربر :" + str(self.user)
        else:
            return self.title + " عدم تحویل به کاربر :" + str(self.user)
