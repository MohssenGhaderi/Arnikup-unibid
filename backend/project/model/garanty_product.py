from project import db
import datetime

garanty_products = db.Table('garanty_products', db.Model.metadata,
    db.Column('garanty_id', db.ForeignKey('garanties.id')),
    db.Column('product_id', db.ForeignKey('products.id'))
)
