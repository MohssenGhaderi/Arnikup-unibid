from project.database import db, Base
import datetime

class Address(Base):
    __tablename__ = 'addresses'

    id = db.Column(db.BigInteger, primary_key=True)
    user = db.relationship('User', uselist=False, back_populates='address')

    country = db.Column(db.String(length=50),nullable=False,default="ایران")

    state_id = db.Column(db.BigInteger, db.ForeignKey('states.id'),nullable=False)
    state = db.relationship('State')

    city = db.Column(db.String(length=50), nullable=False)
    address = db.Column(db.String(length=255), nullable=False)
    postal_code = db.Column(db.String(length=20), nullable=True)

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return " آدرس :" + self.country + " - " + str(self.state) + "  - " + self.city + " - " + self.address
