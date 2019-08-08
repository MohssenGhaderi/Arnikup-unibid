
from project import db
import datetime

class UserActivity(db.Model):
    __tablename__ = 'user_activities'
    id = db.Column(db.BigInteger, primary_key=True)
    activity = db.Column(db.String(length=255), nullable=False)
    ip = db.Column(db.String(length=100), nullable=False)

    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'),nullable=False)
    user = db.relationship('User')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
