from project.database import db, Base
import datetime

class Product(Base):

    __tablename__ = 'products'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=255), nullable=False)
    description = db.Column(db.Text,nullable=False)
    details = db.Column(db.Text)

    category_id = db.Column(db.BigInteger, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='products')

    items = db.relationship('Item')

    # comments = db.relationship("Comment")

    manufacture_id = db.Column(db.BigInteger,db.ForeignKey('manufactures.id'))
    manufacture = db.relationship('Manufacture')

    # advertisement_id = db.Column(db.BigInteger,db.ForeignKey('advertisements.id'))
    # advertisement = db.relationship('Advertisement')

    # inventories = db.relationship('Inventory', secondary='inventory_products' ,back_populates='products')
    #
    # garanties = db.relationship('Garanty', secondary='garanty_products' ,back_populates='products')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title
