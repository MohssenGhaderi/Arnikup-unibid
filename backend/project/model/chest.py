from project.database import db, Base
import datetime

class Chest(Base):
    __tablename__ = 'chests'
    id = db.Column(db.BigInteger,primary_key=True)
    title = db.Column(db.String(length=255), nullable=False)
    description = db.Column(db.Text,nullable=False)
    discount = db.Column(db.Float(),default=0)
    is_active = db.Column(db.Boolean,nullable =False,default=False)
    image = db.Column(db.Text,nullable=True)


    avatars = db.relationship('Avatar', secondary='chest_avatars', back_populates='chests',lazy='dynamic')

    gem_id = db.Column(db.BigInteger, db.ForeignKey('gems.id'))
    gem = db.relationship('Gem')

    coin_id = db.Column(db.BigInteger, db.ForeignKey('coins.id'))
    coin = db.relationship('Coin')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return  self.title
