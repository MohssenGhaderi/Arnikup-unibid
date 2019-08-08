from project import db
import datetime

class Charity(db.Model):
    __tablename__ = 'charities'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100),nullable=False)
    description = db.Column(db.Text,nullable=False)
    icon = db.Column(db.Text,nullable=False)
    is_active = db.Column(db.Boolean,default=False)
    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        return self.title
