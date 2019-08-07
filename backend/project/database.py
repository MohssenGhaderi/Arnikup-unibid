from flask_sqlalchemy import SQLAlchemy
from . import app
from sqlalchemy.ext.declarative import declarative_base
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager


db = SQLAlchemy(app)
Base = db.Model

def init_db():
    from  .model import revoked
    from  .model import address
    from  .model import state
    from  .model import advertisement
    from  .model import auction_plan
    from  .model import auction
    from  .model import category
    from  .model import coupon
    from  .model import insurance
    from  .model import item
    from  .model import manufacture_product
    from  .model import manufacture
    from  .model import bid
    from  .model import order
    from  .model import payment
    from  .model import payment_message
    from  .model import payment_message_payment
    from  .model import plan
    from  .model import product
    from  .model import role
    from  .model import shipment_method
    from  .model import item_shipment
    from  .model import item_garanty
    from  .model import garanty
    from  .model import shipment
    from  .model import user_auction_like
    from  .model import user_auction_participation
    from  .model import user_auction_view
    from  .model import user_coupon
    from  .model import user_plan
    from  .model import user_plan_payment
    from  .model import user_plan_gem_payment
    from  .model import user_plan_coin_payment
    from  .model import user_role
    from  .model import user
    from  .model import user_message
    from  .model import guest_message
    from  .model import notification
    from  .model import auction_notification
    from  .model import site_notification
    from  .model import user_notification
    from  .model import user_auction_notification
    from  .model import user_sms
    from  .model import credit_log
    from  .model import avatar
    from  .model import user_gem
    from  .model import user_coin
    from  .model import chest_avatar
    from  .model import chest
    from  .model import coin
    from  .model import gem
    from  .model import gem_payment
    from  .model import coin_payment
    from  .model import level
    from  .model import user_avatar
    from  .model import user_chest
    from  .model import charity
    from  .model import user_activity
    from  .model import setting

    db.drop_all()
    db.create_all()

    from  .model.role import Role

    role = Role()
    role.name = 'regular'
    role.description = 'this is regular role'
    db.session.add(role)
    db.session.commit()

    role = Role()
    role.name = 'admin'
    role.description = 'this is admin role'
    db.session.add(role)
    db.session.commit()

# print ("initing...")
# init_db()
# print ("done")

def migrate():
    db.create_all()
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    from  .model import revoked
    from  .model import address
    from  .model import state
    from  .model import advertisement
    from  .model import auction_plan
    from  .model import auction
    from  .model import category
    from  .model import coupon
    from  .model import insurance
    from  .model import item
    from  .model import manufacture_product
    from  .model import manufacture
    from  .model import bid
    from  .model import order
    from  .model import payment
    from  .model import payment_message
    from  .model import payment_message_payment
    from  .model import plan
    from  .model import product
    from  .model import role
    from  .model import shipment_method
    from  .model import item_shipment
    from  .model import item_garanty
    from  .model import garanty
    from  .model import shipment
    from  .model import user_auction_like
    from  .model import user_auction_participation
    from  .model import user_auction_view
    from  .model import user_coupon
    from  .model import user_plan
    from  .model import user_plan_payment
    from  .model import user_plan_gem_payment
    from  .model import user_plan_coin_payment
    from  .model import user_role
    from  .model import user
    from  .model import user_message
    from  .model import guest_message
    from  .model import notification
    from  .model import auction_notification
    from  .model import site_notification
    from  .model import user_notification
    from  .model import user_auction_notification
    from  .model import user_sms
    from  .model import credit_log
    from  .model import avatar
    from  .model import user_gem
    from  .model import user_coin
    from  .model import chest_avatar
    from  .model import chest
    from  .model import coin
    from  .model import gem
    from  .model import gem_payment
    from  .model import coin_payment
    from  .model import level
    from  .model import user_avatar
    from  .model import user_chest
    from  .model import charity
    from  .model import user_activity
    from  .model import setting
    manager.run()
#
# print ("migrating ... ")
# migrate()
# print ("migration done..!")
