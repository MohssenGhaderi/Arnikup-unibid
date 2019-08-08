from project import db
import datetime

class ItemGaranty(db.Model):
    __tablename__ = 'item_garanties'

    id = db.Column(db.BigInteger,primary_key=True)
    price = db.Column(db.DECIMAL(precision=20, scale=4),nullable=False)

    item_id = db.Column(db.BigInteger, db.ForeignKey('items.id'))
    item = db.relationship('Item',cascade="all,delete")

    garanty_id = db.Column(db.BigInteger, db.ForeignKey('garanties.id'))
    garanty = db.relationship('Garanty',cascade="all,delete")

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        try:
            return "گارانتی محصول" + self.item.title + " گارانتی " + self.garanty.title + "باهزینه " + self.price
        except Exception as e:
            return "بدون عنوان"
