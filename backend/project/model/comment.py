from project import db
import datetime

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    likes = db.Column(db.Integer, default=0)

    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'))
    user = db.relationship('User')

    product_id = db.Column(db.BigInteger, db.ForeignKey('products.id'))
    product = db.relationship('Product')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title + " متن پیام :" + self.message
