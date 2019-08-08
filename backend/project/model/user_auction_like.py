from project import db
import datetime

user_auction_likes = db.Table('user_auction_likes', db.Model.metadata,
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('auction_id', db.ForeignKey('auctions.id')),
    db.Column('date',db.TIMESTAMP, default=datetime.datetime.now)
)
