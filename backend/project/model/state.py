
from project.database import db, Base
import datetime

class State(Base):
    __tablename__ = 'states'
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(length=50), nullable=False)
    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return self.title
