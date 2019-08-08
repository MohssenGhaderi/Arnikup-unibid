from project import db
import datetime

class Advertisement(db.Model):
    __tablename__ = 'advertisements'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100),nullable=False)
    description = db.Column(db.Text,nullable=False)
    image = db.Column(db.Text,nullable=True)
    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
    def __str__(self):
        return self.title
