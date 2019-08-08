from project import db
import datetime

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=255),nullable=False)
    description = db.Column(db.Text,nullable=False)
    start_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    end_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    is_active = db.Column(db.Boolean,default=False)
    discount = db.Column(db.Integer,nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        return self.title
