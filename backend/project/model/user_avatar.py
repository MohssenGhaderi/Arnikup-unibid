
from project import db
import datetime

class UserAvatar(db.Model):
    __tablename__ = 'user_avatars'
    __table_args__ = (db.UniqueConstraint('user_id', 'avatar_id', name='UC_user_id_avatar_id'),)

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
