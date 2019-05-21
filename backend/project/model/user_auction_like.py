from project.database import db, Base
import datetime

user_auction_likes = db.Table('user_auction_likes', Base.metadata,
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('auction_id', db.ForeignKey('auctions.id')),
    db.Column('date',db.TIMESTAMP, default=datetime.datetime.now)
)
