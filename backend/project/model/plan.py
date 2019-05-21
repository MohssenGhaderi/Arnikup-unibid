from project.database import db, Base
import datetime

class Plan(Base):
    __tablename__ = 'plans'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    auctions = db.relationship('AuctionPlan')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title
