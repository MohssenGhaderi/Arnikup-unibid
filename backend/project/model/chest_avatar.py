from project import db
import datetime

user_gifts = db.Table('chest_avatars', db.Model.metadata,
    db.Column('chest_id', db.ForeignKey('chests.id')),
    db.Column('avatar_id', db.ForeignKey('avatars.id'))
)
