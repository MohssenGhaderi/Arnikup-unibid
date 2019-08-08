from project import db
import datetime

class Manufacture(db.Model):
    __tablename__ = 'manufactures'
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(length=25), nullable=False)
    country = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    details =  db.Column(db.Text, nullable=True)
    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.name
