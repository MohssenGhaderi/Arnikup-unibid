
from project.database import db, Base
import datetime

class Level(Base):
    __tablename__ = 'levels'
    __table_args__ = (db.UniqueConstraint('number', name='levels_number_uc'),)

    id = db.Column(db.BigInteger,primary_key=True)
    title = db.Column(db.String(length=255), nullable=False)
    number = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.Text,nullable=False)
    required_points = db.Column(db.Integer(),default=0,nullable=False)
    offered_gems = db.Column(db.Integer(),default=0,nullable=False)
    points_per_win = db.Column(db.Integer(),default=0)
    image = db.Column(db.Text,nullable=False)

    users = db.relationship("User")
    auctions = db.relationship("Auction")

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return  self.title +" شامل "+  str(self.required_points) + " امتیاز "
