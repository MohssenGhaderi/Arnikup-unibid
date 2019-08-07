from project.database import db, Base
import datetime
import time
import random
from passlib.hash import pbkdf2_sha256 as sha256
from flask_login import UserMixin
from definitions import BASE_USER_CREDIT
from  .role import Role



class User(Base,UserMixin):
    def __init__(self, username):
        try:
             return cls.query.get(uid)
        except:
         return None

    random.seed(time.time())
    __tablename__ = 'users'
    __table_args__ = (db.UniqueConstraint('username', name='users_username_uc'),)
    __table_args__ = (db.UniqueConstraint('mobile', name='users_mobilr_uc'),)

    id = db.Column(db.BigInteger, primary_key=True)

    activation_code = db.Column(db.String(length=10), nullable=False, default = random.randint(100000,1000000))
    is_verified = db.Column(db.Boolean,nullable =False,default=False)
    is_active = db.Column(db.Boolean,nullable =False,default=True)
    is_banned = db.Column(db.Boolean,nullable =False,default=False)
    verification_attempts = db.Column(db.Integer,nullable =False,default=0)
    login_attempts = db.Column(db.Integer,nullable =False,default=0)
    send_sms_attempts = db.Column(db.Integer,nullable =False,default=0)
    username = db.Column(db.String(length=255), nullable=False)
    # alias_name = db.Column(db.String(128), nullable = True)
    full_name = db.Column(db.String(length=100))
    # first_name = db.Column(db.String(length=100))
    # last_name = db.Column(db.String(length=100))
    work_place = db.Column(db.String(length=100))
    mobile = db.Column(db.String(length=15), nullable=False)
    email = db.Column(db.String(length=255))
    password = db.Column(db.String(length=100), nullable=False)

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)

    invitor = db.Column(db.String(length=255))
    points = db.Column(db.Integer(),default=0,nullable=False)
    coins = db.Column(db.Integer(),default=0,nullable=False)
    gems = db.Column(db.Integer(),default=0,nullable=False)

    address_id = db.Column(db.BigInteger, db.ForeignKey('addresses.id'))
    address = db.relationship('Address')

    avatars = db.relationship('Avatar', secondary='user_avatars', back_populates='users',lazy='dynamic')


    plans = db.relationship('UserPlan',lazy='dynamic')
    user_gems = db.relationship('UserGem',lazy='dynamic')

    payments = db.relationship('Payment')
    gem_payments = db.relationship('GemPayment')
    
    messages = db.relationship('UserMessage',lazy='dynamic')

    short_messages = db.relationship('UserSMS')

    orders = db.relationship('Order')

    roles = db.relationship('Role' , secondary = 'user_roles', back_populates='users')

    coupons = db.relationship('Coupon', secondary='user_coupons', back_populates='users',lazy='dynamic')

    level_id = db.Column(db.BigInteger, db.ForeignKey('levels.id'))
    level = db.relationship('Level')

    avatar_id = db.Column(db.BigInteger, db.ForeignKey('avatars.id'))
    avatar = db.relationship('Avatar')

    notifications = db.relationship('Notification', secondary='user_notifications', back_populates='users',lazy='dynamic')

    auctions = db.relationship('Auction', lazy='dynamic', secondary='user_auction_participations',back_populates='participants')

    auction_views = db.relationship('Auction', secondary ='user_auction_views', back_populates='views')
    auction_likes = db.relationship('Auction', secondary ='user_auction_likes', back_populates='likes',lazy='dynamic')

    def __str__(self):
        return self.username

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    @classmethod
    def find_by_mobile(cls, mobile):
        return cls.query.filter_by(mobile = mobile).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def is_admin(self):
        admin = False
        for role in self.roles:
            if( role.name == 'admin' ):
                admin = True
        return admin

    def has_auction(self,id):
        try:
            return next(a for a in self.auctions if a.id == id)
        except Exception as e:
            return None

    def has_role(self,name):
        try:
            return next(a for a in self.roles if a.name == name),None
        except Exception as e:
            return None

    def save_to_db(self):
        #add default role to created user
        role = Role.query.filter_by(name='regular').first()
        if(role):
            self.roles.append(role)
            db.session.add(self)
            db.session.commit()

# @validates('username')
# def validate_username(self, key, username):
#   if not username:
#       raise AssertionError('No username provided')
#
#   if User.query.filter(User.username == username).first():
#     raise AssertionError('Username is already in use')
#
#   if len(username) < 5 or len(username) > 20:
#     raise AssertionError('Username must be between 5 and 20 characters')
#
#   return username
#
# @validates('email')
# def validate_email(self, key, email):
#   if not email:
#     raise AssertionError('No email provided')
#
#   if not re.match("[^@]+@[^@]+\.[^@]+", email):
#     raise AssertionError('Provided email is not an email address')
#
#   return email
