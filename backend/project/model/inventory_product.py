from project import db

inventory_products = db.Table('inventory_products', db.Model.metadata,
    db.Column('inventory_id', db.ForeignKey('inventories.id')),
    db.Column('product_id', db.ForeignKey('products.id')),
)
