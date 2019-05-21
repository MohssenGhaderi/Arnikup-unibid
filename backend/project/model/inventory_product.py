from project.database import db, Base

inventory_products = db.Table('inventory_products', Base.metadata,
    db.Column('inventory_id', db.ForeignKey('inventories.id')),
    db.Column('product_id', db.ForeignKey('products.id')),
)
