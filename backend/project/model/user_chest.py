

from project import db
import datetime

class UserChest(db.Model):
    __tablename__ = 'user_chests'
    id = db.Column(db.BigInteger,primary_key=True)
    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')

    chest_id = db.Column(db.BigInteger,db.ForeignKey('chests.id'))
    chest = db.relationship('Chest')

    payment_id = db.Column(db.BigInteger,db.ForeignKey('payments.id'))
    payment = db.relationship('Payment',cascade="all,delete",backref="user_chests")

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        if(self.user):
            return " بسته پیشنهادی " + self.chest.title +" به قیمت "+ str(self.payment.amount) + " به کاربر "+ self.user.username + " اختصاص دارد "
        return self.chest.title
