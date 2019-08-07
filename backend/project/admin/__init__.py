
from ..database import db
from .. import app
from .classes import *
from ..model import *
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from passlib.hash import pbkdf2_sha256 as sha256
from flask_security import current_user, login_required
# # Initialize the SQLAlchemy data store and quart-Security.
# user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(app, user_datastore)

# Create admin
admin = Admin(
    app," یونی بید ",index_view=MyAdminIndexView(),base_template='admin.html',template_mode='bootstrap3',
)
admin.add_view(UserAdmin(User, db.session,name='کاربران',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(RoleAdmin(Role, db.session,name='نقش',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(CategoryAdmin(Category, db.session,name='دسته بندی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ProductAdmin(Product, db.session,name='محصولات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ItemAdmin(Item, db.session,name='آیتم های محصولات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(AuctionAdmin(Auction, db.session,name='حراجی ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(BidAdmin(Bid, db.session,name='بیدهای کاربران',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(PlanAdmin(Plan, db.session,name='پلن های پیش فرض',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(AuctionPlanAdmin(AuctionPlan, db.session,name='پلن حراجی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(AvatarAdmin(Avatar, db.session,name='آواتارها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(CoinAdmin(Coin, db.session,name='بسته های سکه',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(GemAdmin(Gem, db.session,name='بسته های الماس',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ChestAdmin(Chest, db.session,name='پکیج های پیشنهادی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(LevelAdmin(Level, db.session,name='مراحل',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(AdvertisementAdmin(Advertisement, db.session,name='تبلیغات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(CharityAdmin(Charity, db.session,name='خیریه ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ShipmentMethodAdmin(ShipmentMethod, db.session,name='روش ارسال پیش فرض',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ShipmentAdmin(Shipment, db.session,name='گزارش ارسال ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ItemShipmentAdmin(ItemShipment, db.session,name='روش ارسال محصولات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(GarantyAdmin(Garanty, db.session,name='گارانتی ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ItemGarantyAdmin(ItemGaranty, db.session,name='گارانتی محصولات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(InsuranceAdmin(Insurance, db.session,name='بیمه',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(CouponAdmin(Coupon, db.session,name='کوپن تخفیف های سایت',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(ManufactureAdmin(Manufacture, db.session,name='کارخانه ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(StateAdmin(State, db.session,name='استان ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserAuctionParticipationAdmin(UserAuctionParticipation, db.session,name='گزارش شرکت کنندگان حراجی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserPlanAdmin(UserPlan, db.session,name='گزارش پلن حراجی کاربر',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserPlanPaymentAdmin(UserPlanPayment, db.session,name='گزارش خرید پلن با درگاه پرداخت',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserPlanCoinPaymentAdmin(UserPlanCoinPayment, db.session,name='گزارش خرید پلن با سکه',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserPlanGemPaymentAdmin(UserPlanGemPayment, db.session,name='گزارش خرید پلن با الماس',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserAvatarAdmin(UserAvatar, db.session,name='گزارش خرید اوتار با الماس',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserCoinAdmin(UserCoin, db.session,name='گزارش سکه های خریداری شده کاربران',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserGemAdmin(UserGem, db.session,name='گزارش الماس های خریداری شده کاربران',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserChestAdmin(UserChest, db.session,name='گزارش پکیج های پیشنهادی خریداری شده کاربران',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(PaymentAdmin(Payment, db.session,name='گزارش پرداخت های درگاه',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(GemPaymentAdmin(GemPayment, db.session,name='گزارش پرداخت الماس',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(CoinPaymentAdmin(CoinPayment, db.session,name='گزارش پرداخت های سکه',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(OrderAdmin(Order, db.session,name='گزارش سفارشات',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserCouponAdmin(UserCoupon, db.session,name='گزارش کوپن های تخفیف کاربران',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(PaymentMessageAdmin(PaymentMessage, db.session,name='پیام پرداختی های سایت',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserActivityAdmin(UserActivity, db.session,name='گزارش فعالیت های کاربران',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(AddressAdmin(Address, db.session,name='گزارش آدرس های کاربران',menu_icon_type='fa', menu_icon_value='fa fa-user'))
# admin.add_view(SettingAdmin(Setting, db.session,name='تنظیمات',menu_icon_type='fa', menu_icon_value='fa fa-user'))

admin.add_view(NotificationAdmin(Notification, db.session,name='ناتیفیکیشن ها',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(SiteNotificationAdmin(SiteNotification, db.session,name='گزارش ناتیفیکیشن های سایت',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserNotificationAdmin(UserNotification, db.session,name='گزارش ناتیفیکیشن های کاربران',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(AuctionNotificationAdmin(AuctionNotification, db.session,name='ایجاد ناتیفیکیشن حراجی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(UserMessageAdmin(UserMessage, db.session,name='پیام های کاربران سایت',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(GuestMessageAdmin(GuestMessage, db.session,name='پیام های کاربران مهمان',menu_icon_type='fa', menu_icon_value='fa fa-user'))
admin.add_view(SMSAdmin(UserSMS, db.session,name='گزارش پیامک های ارسالی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
# admin.add_view(UserAuctionNotificationAdmin(UserAuctionNotification, db.session,name='ناتیفیکیشن کاربران حراجی',menu_icon_type='fa', menu_icon_value='fa fa-user'))
# admin.add_view(CreditLogAdmin(CreditLog, db.session,name='لاگ اعتبارات کاربر',menu_icon_type='fa', menu_icon_value='fa fa-user'))
