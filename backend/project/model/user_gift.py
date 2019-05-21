from project.database import db, Base
import datetime

user_gifts = db.Table('user_gifts', Base.metadata,
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('gift_id', db.ForeignKey('gifts.id')),
    db.Column('used',db.Boolean,default=False)
)
