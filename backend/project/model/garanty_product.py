from project.database import db, Base
import datetime

garanty_products = db.Table('garanty_products', Base.metadata,
    db.Column('garanty_id', db.ForeignKey('garanties.id')),
    db.Column('product_id', db.ForeignKey('products.id'))
)
