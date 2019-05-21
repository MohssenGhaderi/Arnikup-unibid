
from project.database import db, Base
import datetime


class Setting(Base):
    __tablename__ = 'settings'
    id = db.Column(db.BigInteger,primary_key=True)
    default_coupon = db.Column(db.String(length=255), nullable=False)
    base_bid_price = db.Column(db.Integer(),default=0,nullable=False)
    base_coin_price = db.Column(db.Integer(),default=0,nullable=False)
    base_gem_price = db.Column(db.Integer(),default=0,nullable=False)
    session_expire_time = db.Column(db.Integer(),default=0,nullable=False)
    max_orders = db.Column(db.Integer(),default=0,nullable=False)
    max_search_results = db.Column(db.Integer(),default=0,nullable=False)

    sms_service_number = db.Column(db.String(length=255), nullable=False)
    sms_username = db.Column(db.String(length=255), nullable=False)
    sms_password = db.Column(db.String(length=255), nullable=False)

    sms_code_ver = db.Column(db.Integer(),default=0,nullable=False)
    sms_code_wel = db.Column(db.Integer(),default=0,nullable=False)
    sms_code_fps = db.Column(db.Integer(),default=0,nullable=False)
    sms_code_chps = db.Column(db.Integer(),default=0,nullable=False)
    sms_code_ginv = db.Column(db.Integer(),default=0,nullable=False)
    sms_code_gusr = db.Column(db.Integer(),default=0,nullable=False)

    max_activation_attempts = db.Column(db.Integer(),default=0,nullable=False)
    max_login_attempts = db.Column(db.Integer(),default=0,nullable=False)
    max_sms_send_attempts = db.Column(db.Integer(),default=0,nullable=False)

    max_deffer_activation_time = db.Column(db.Integer(),default=0,nullable=False)
    max_available_verify_time = db.Column(db.Integer(),default=0,nullable=False)

    max_invitors_policy = db.Column(db.Integer(),default=0,nullable=False)
    max_messages_policy = db.Column(db.Integer(),default=0,nullable=False)

    created = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False)
    updated = db.Column(db.TIMESTAMP, default=datetime.datetime.now, nullable=False, onupdate=datetime.datetime.now)
