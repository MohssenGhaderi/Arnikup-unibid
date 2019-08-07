

from project.database import db, Base
import datetime

class UserGem(Base):
    __tablename__ = 'user_gems'
    id = db.Column(db.BigInteger,primary_key=True)
    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')

    gem_id = db.Column(db.BigInteger,db.ForeignKey('gems.id'))
    gem = db.relationship('Gem')

    payment_id = db.Column(db.BigInteger,db.ForeignKey('payments.id'))
    payment = db.relationship('Payment',cascade="all,delete",backref="user_gems")

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        if(self.user):
            return " الماس " + self.gem.title +" به قیمت "+ str(self.gem.price) + " به کاربر "+ self.user.username + " اختصاص دارد "
        return self.gem.title
