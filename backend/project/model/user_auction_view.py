from project import db
import datetime


user_auction_views = db.Table('user_auction_views', db.Model.metadata,
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('auction_id', db.ForeignKey('auctions.id')),
    db.Column('count',db.Integer()),
    db.Column('ip',db.String(length=50)),
    db.Column('date',db.TIMESTAMP, default=datetime.datetime.now)
)
