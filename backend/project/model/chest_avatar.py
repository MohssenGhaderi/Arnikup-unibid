from project.database import db, Base
import datetime

user_gifts = db.Table('chest_avatars', Base.metadata,
    db.Column('chest_id', db.ForeignKey('chests.id')),
    db.Column('avatar_id', db.ForeignKey('avatars.id'))
)
