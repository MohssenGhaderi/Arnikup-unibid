from project import db
import datetime

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.String(length=255),nullable=False)
    icon = db.Column(db.Text,nullable=False)
    parent_id = db.Column(db.BigInteger, db.ForeignKey('categories.id'))
    parent = db.relationship('Category', remote_side=[id])
    products = db.relationship('Product', back_populates = 'category')
    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title
