from project import db
import datetime

class Auction(db.Model):
    __tablename__ = 'auctions'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    image = db.Column(db.Text)
    tag = db.Column(db.String(255))
    description = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean,nullable =False,default=True)
    done = db.Column(db.Boolean,default=False)
    start_date = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    base_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    max_price = db.Column(db.DECIMAL(precision=20, scale=4), nullable=False)
    max_members = db.Column(db.BigInteger,default=10,nullable=False)
    min_members = db.Column(db.BigInteger,default=0,nullable=False)
    ratio = db.Column(db.Integer,default=1,nullable=False)

    have_extra_gems = db.Column(db.Boolean,nullable =False,default=False)
    extra_bids = db.Column(db.Integer,default=0,nullable=False)
    required_gems = db.Column(db.Integer,default=0,nullable=False)
    target_bid = db.Column(db.Integer,default=3)

    item_id = db.Column(db.BigInteger, db.ForeignKey('items.id'),nullable=False)
    item = db.relationship('Item')

    participants = db.relationship('User',secondary='user_auction_participations',lazy='dynamic',back_populates='auctions')

    views = db.relationship('User', secondary = 'user_auction_views', lazy='dynamic', back_populates='auction_views')
    likes = db.relationship('User', secondary = 'user_auction_likes', lazy='dynamic', back_populates='auction_likes')

    level_id = db.Column(db.BigInteger, db.ForeignKey('levels.id'))
    level = db.relationship('Level')

    advertisement_id = db.Column(db.BigInteger,db.ForeignKey('advertisements.id'))
    advertisement = db.relationship('Advertisement')

    charity_id = db.Column(db.BigInteger,db.ForeignKey('charities.id'))
    charity = db.relationship('Charity')

    plans = db.relationship('AuctionPlan' ,lazy='dynamic')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title
