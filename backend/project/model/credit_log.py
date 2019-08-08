from project import db

import datetime

class CreditLog(db.Model):
    __tablename__ = 'user_credit_logs'

    id = db.Column(db.BigInteger,primary_key=True)

    before_credit = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    after_credit = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)

    user_id = db.Column(db.BigInteger,db.ForeignKey('users.id'))
    user = db.relationship('User')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
