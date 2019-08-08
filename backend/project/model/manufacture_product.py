from project import db
import datetime

manufacture_products = db.Table('manufacture_products', db.Model.metadata,
    db.Column('manufacture_id', db.ForeignKey('manufactures.id')),
    db.Column('product_id', db.ForeignKey('products.id'))
)
