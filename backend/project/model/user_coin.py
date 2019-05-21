

from project.database import db, Base
import datetime

class UserCoin(Base):
    __tablename__ = 'user_coins'
    id = db.Column(db.BigInteger,primary_key=True)
    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')

    coin_id = db.Column(db.BigInteger,db.ForeignKey('coins.id'))
    coin = db.relationship('Coin')

    payment_id = db.Column(db.BigInteger,db.ForeignKey('payments.id'))
    payment = db.relationship('Payment')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        if(self.user):
            return " سکه " + self.coin.title +" به قیمت "+ str(self.coin.price) + " به کاربر "+ self.user.username + " اختصاص دارد "
        return self.coin.title
