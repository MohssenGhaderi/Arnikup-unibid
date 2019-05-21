
from project.database import db, Base
import datetime

class Item(Base):
    __tablename__ = 'items'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text(),nullable=False)
    price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    quantity = db.Column(db.Integer(),default=0,nullable=False)
    discount = db.Column(db.Integer(),default=0,nullable=False)
    details = db.Column(db.Text())
    images = db.Column(db.Text, nullable=False)

    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'),nullable=False)
    product = db.relationship('Product')

    orders = db.relationship('Order')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        return  " محصول :"+str(self.product.title) + " آیتم: " + self.title
        # return  'نام محصول'
