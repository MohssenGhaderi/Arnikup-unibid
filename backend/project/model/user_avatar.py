
from project.database import db, Base
import datetime

class UserAvatar(Base):
    __tablename__ = 'user_avatars'
    id = db.Column(db.BigInteger,primary_key=True)
    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')

    avatar_id = db.Column(db.BigInteger,db.ForeignKey('avatars.id'))
    avatar = db.relationship('Avatar')

    gem_payment_id = db.Column(db.BigInteger,db.ForeignKey('gem_payments.id'))
    gem_payment = db.relationship('GemPayment')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        if(self.user):
            return " آواتار " + self.avatar.title +" به قیمت "+ str(self.avatar.price) + " به کاربر "+ self.user.username + " اختصاص دارد "
        return self.avatar.title
