from project.database import db, Base
import datetime


class Gift(Base):
    __tablename__ = 'gifts'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    expired = db.Column(db.Boolean,default=False)

    users = db.relationship('User', secondary='user_gifts', back_populates='gifts',lazy='dynamic')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    # def __str__(self):
    #     return self.title
