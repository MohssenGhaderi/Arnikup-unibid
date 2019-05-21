
from project.database import db, Base
import datetime

class AvatarType:
    REGULAR = 'عمومی'
    PRIVATE = 'اختصاصی'

class Avatar(Base):
    __tablename__ = 'avatars'
    id = db.Column(db.BigInteger,primary_key=True)
    title = db.Column(db.String(length=255), nullable=False)
    description = db.Column(db.Text,nullable=False)
    image = db.Column(db.Text,nullable=False)
    needed_gems = db.Column(db.Integer(),default=0,nullable=False)
    type = db.Column(db.String(64),default=AvatarType.REGULAR)

    chests = db.relationship('Chest', secondary='chest_avatars', back_populates='avatars',lazy='dynamic')

    users = db.relationship('User',secondary='user_avatars',lazy='dynamic',back_populates='avatars')

    # gem_pay_id = db.Column(db.BigInteger,db.ForeignKey('gem_payments.id'))
    # gem_pay = db.relationship('Gempay')

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    def __str__(self):
        return  self.title + " از نوع " + str(self.type) + " با " + str(self.needed_gems) + " عدد الماس "
