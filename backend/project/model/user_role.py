from project import db
import datetime

user_roles = db.Table('user_roles', db.Model.metadata,
    db.Column('user_id', db.ForeignKey('users.id')),
    db.Column('role_id', db.ForeignKey('roles.id'))
)
