import random
from markupsafe import Markup
from flask import url_for,render_template,abort,session,redirect
from flask_admin import AdminIndexView
from flask_admin import expose,form
from functools import wraps
from ..middleware import has_role
from flask_security import current_user
from flask_admin.contrib.sqla import ModelView
from wtforms import StringField,SelectField,BooleanField
from .utils import MultipleImageUploadField
from . import app
from PIL import Image
import ast
from ..model import *
from sqlalchemy import or_ , and_
from sqlalchemy import func
from project.database import db

def checkAdmin(role):
    return True
    return current_user.has_role(role)

class MyAdminIndexView(AdminIndexView):

    @expose('/admin/', methods=('GET', 'POST'))
    def edit_view(self):
         users = User.query.count()
         print ("users :",users)
         return super(AdminIndexView, users=users).edit_view()

    def is_accessible(self):
        return checkAdmin('admin')

    @expose('/')
    def index(self):
        # auctions = Auction.query.count() + 1
        # users = User.query.count()
        # payments = Payment.query.count()
        # orders = Order.query.count()
        # user_auction_participants = User.query.join(UserAuctionParticipation).count()
        # online_payments = db.session.query(func.sum(Payment.amount).label('total')).filter_by(status=PaymentStatus.ARCHIVE).scalar()
        # wallet_charge = db.session.query(func.sum(Payment.amount).label('total')).filter_by(status=PaymentStatus.ARCHIVE,type=PaymentType.WALET).scalar()
        # buy_plan = db.session.query(func.sum(Payment.amount).label('total')).filter_by(status=PaymentStatus.ARCHIVE,type=PaymentType.PLAN).scalar()
        # buy_product = db.session.query(func.sum(Payment.amount).label('total')).filter_by(status=PaymentStatus.ARCHIVE,type=PaymentType.PRODUCT).scalar()
        # free_payments = AuctionPlan.query.filter_by(coins=0).count()
        # total_shipment_walet = db.session.query((func.sum(ShipmentMethod.price).label('total'))).join(Shipment).join(Order).join(Payment).filter(Payment.status==PaymentStatus.ARCHIVE,Payment.type==PaymentType.PRODUCT,Payment.payment_method_id==2).scalar()
        # total_shipment_online = db.session.query((func.sum(ShipmentMethod.price).label('total'))).join(Shipment).join(Order).join(Payment).filter(Payment.status==PaymentStatus.ARCHIVE,Payment.type==PaymentType.PRODUCT,Payment.payment_method_id==1).scalar()
        # paid_shipment = Shipment.query.join(Order).join(Payment).filter(Payment.status==PaymentStatus.ARCHIVE,Payment.type==PaymentType.PRODUCT).count()
        # online_payment_discounts = db.session.query(func.sum(Payment.discount).label('total')).filter_by(status=PaymentStatus.ARCHIVE).scalar()
        #
        # passed_auctions = Offer.query.filter_by(won=True).count() + 1
        # avg_auction_users = ("%.2f" % (float(user_auction_participants)/float(auctions)))
        # avg_participated_auction_users = ("%.2f" % (float(user_auction_participants)/float(passed_auctions)))
        #
        #
        # all_wons = 0
        # items_total_price = 0
        # offers = Offer.query.filter_by(won=True).all()
        # for offer in offers:
        #     all_wons += offer.total_price
        #     items_total_price += offer.auction.item.price
        #
        #
        # self._template_args['auctions'] = auctions
        # self._template_args['passed_auctions'] = passed_auctions
        # self._template_args['users'] = users
        # self._template_args['payments'] = payments
        # self._template_args['orders'] = orders
        # self._template_args['user_auction_participants'] = user_auction_participants
        # self._template_args['avg_auction_users'] = avg_auction_users
        # self._template_args['avg_participated_auction_users'] = avg_participated_auction_users
        # self._template_args['online_payments'] = int(online_payments*3)
        # self._template_args['wallet_charge'] = int(wallet_charge*3)
        # self._template_args['buy_plan'] = int(buy_plan*3)
        # self._template_args['free_payments'] = free_payments
        # self._template_args['paid_shipment'] = paid_shipment
        # self._template_args['online_payment_discounts'] = int(online_payment_discounts*3)
        # self._template_args['potantial_discounts'] = int(items_total_price - all_wons)
        #
        # if buy_product:
        #     self._template_args['buy_product'] = int(buy_product*3)
        # else:
        #     self._template_args['buy_product'] = 0
        #
        # if total_shipment_walet:
        #     self._template_args['total_shipment_walet'] = int(total_shipment_walet*3)
        # else:
        #     self._template_args['total_shipment_walet'] = 0
        #
        # if total_shipment_online:
        #     self._template_args['total_shipment_online'] = int(total_shipment_online*3)
        # else:
        #     self._template_args['total_shipment_online'] = 0
        #
        #
        return super(MyAdminIndexView, self).index()

class VerifiedBooleanField(SelectField):
    def __init__(self, *args, **kwargs):
        choices = [
            (False,'عدم تایید'),
            (True,'تایید شده')
        ]
        kwargs["choices"] = choices
        kwargs["coerce"] = lambda x: str(x) == "True"
        super(VerifiedBooleanField, self).__init__(*args, **kwargs)

class ActiveBooleanField(SelectField):
    def __init__(self, *args, **kwargs):
        choices = [
            (False,'کاربر غیرفعال'),
            (True,'کاربر فعال')
        ]
        kwargs["choices"] = choices
        kwargs["coerce"] = lambda x: str(x) == "True"
        super(ActiveBooleanField, self).__init__(*args, **kwargs)

class BanBooleanField(SelectField):
    def __init__(self, *args, **kwargs):
        choices = [
            (False,'کاربر مجاز'),
            (True,'کاربر بن شده')
        ]
        kwargs["choices"] = choices
        kwargs["coerce"] = lambda x: str(x) == "True"
        super(BanBooleanField, self).__init__(*args, **kwargs)

class UserAdmin(ModelView):
    form_overrides = {
        "is_verified": VerifiedBooleanField,
        "is_active": ActiveBooleanField,
        "is_banned": BanBooleanField,
    }

    form_excluded_columns = ('created', 'updated','password','payments','gem_payments','messages','short_messages','orders','gifts','plans','notifications','auction_views','user_gems')

    page_size = 20
    can_view_details = True
    column_searchable_list = ['full_name', 'username','mobile','address.city','address.state.title','address.address','address.postal_code']
    column_editable_list = ['full_name', 'mobile','verification_attempts','login_attempts','send_sms_attempts','coins','gems','points']
    column_exclude_list = ('work_place','password')

    def is_accessible(self):
        return checkAdmin('admin')

class RoleAdmin(ModelView):
    form_excluded_columns = ('created','updated')
    def is_accessible(self):
        return checkAdmin('admin')

class ItemAdmin(ModelView):
    form_excluded_columns = ('created','updated')

    page_size = 20
    can_view_details = True
    column_searchable_list = ['title', 'description']
    column_editable_list = ['title', 'description','price','quantity','discount']
    column_exclude_list = ('description')

    form_widget_args = {
    'description': {
    'rows': 10,
    'style': 'color: black'
    }
    }

    def is_accessible(self):
        return checkAdmin('admin')

    def _list_thumbnail(view, context, model, name):
        if not model.images:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/products/" + form.thumbgen_filename(model.images).split("'")[1]))

        return Markup("<br />".join(gen_img(model.images) for image in ast.literal_eval(model.images)))

    column_formatters = {'images': _list_thumbnail}

    form_extra_fields = {'images': MultipleImageUploadField("Images",
                                                            base_path="project/static/images/products",
                                                            url_relative_path="images/products/",
                                                            thumbnail_size=(64, 64, 1))}

class ShowAdsField(SelectField):
    def __init__(self, *args, **kwargs):
        choices = [
            (False,'عدم نمایش تبلیغ'),
            (True,'نمایش تبلیغ')
        ]
        kwargs["choices"] = choices
        kwargs["coerce"] = lambda x: str(x) == "True"
        super(ShowAdsField, self).__init__(*args, **kwargs)

class AdvertisementAdmin(ModelView):
    form_overrides={
    'show':ShowAdsField
    }

    page_size = 10
    can_view_details = True
    column_searchable_list = ['title', 'description']
    column_editable_list = ['title', 'description']
    def is_accessible(self):
        return True
        return current_user.has_role('admin')

    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/ads/" + form.thumbgen_filename(model.image).split("'")[1]))

        return Markup("<br />".join(gen_img(model.image) for image in ast.literal_eval(model.image)))

    column_formatters = {'image': _list_thumbnail}

    form_extra_fields = {'image': MultipleImageUploadField("Image",
                                                            base_path="project/static/images/ads",
                                                            url_relative_path="images/ads/",
                                                            thumbnail_size=(64, 128, 1))}

class CategoryAdmin(ModelView):

    page_size = 10
    can_view_details = True
    column_searchable_list = ['title', 'description']
    column_editable_list = ['title', 'description']
    form_excluded_columns = ('created','updated','products')
    column_exclude_list = ('description')

    def is_accessible(self):
        return True
        return current_user.has_role('admin')

    def _list_thumbnail(view, context, model, name):
        if not model.icon:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/icons/category/" + form.thumbgen_filename(model.icon).split("'")[1]))

        return Markup("<br />".join(gen_img(model.icon) for image in ast.literal_eval(model.icon)))

    column_formatters = {'icon': _list_thumbnail}

    form_extra_fields = {'icon': MultipleImageUploadField("icon",
                                                            base_path="project/static/images/icons/category",
                                                            url_relative_path="images/icons/category/",
                                                            thumbnail_size=(64, 64, 1))}

class ProductAdmin(ModelView):
    form_excluded_columns = ('created','updated','items')
    page_size = 20
    can_view_details = True
    column_searchable_list = ['title', 'description']
    column_editable_list = ['title', 'description']
    column_exclude_list = ['description','details']

    form_widget_args = {
    'description': {
    'rows': 10,
    'style': 'color: black'
    }
    }

    def is_accessible(self):
        return checkAdmin('admin')

class ExtraGemBooleanField(SelectField):
    def __init__(self, *args, **kwargs):
        choices = [
            (False,'عدم پیشنهاد الماس'),
            (True,'پیشنهاد الماس در حراجی')
        ]
        kwargs["choices"] = choices
        kwargs["coerce"] = lambda x: str(x) == "True"
        super(ExtraGemBooleanField, self).__init__(*args, **kwargs)

class ActiveAuctionBooleanField(SelectField):
    def __init__(self, *args, **kwargs):
        choices = [
            (False,'حراجی غیرفعال'),
            (True,'حراجی فعال')
        ]
        kwargs["choices"] = choices
        kwargs["coerce"] = lambda x: str(x) == "True"
        super(ActiveAuctionBooleanField, self).__init__(*args, **kwargs)

class AuctionAdmin(ModelView):
    form_overrides = {
        "is_active": ActiveAuctionBooleanField,
        "have_extra_gems": ExtraGemBooleanField,
    }

    form_columns = (
    'item', 'level','advertisement','charity',
    'title','description','start_date','base_price','max_price','max_members','ratio',
    'tag','is_active','have_extra_gems','extra_bids','required_gems','done'
    )

    page_size = 20
    can_view_details = True
    column_searchable_list = ['title', 'description']
    column_editable_list = ['title', 'description','start_date','max_price','base_price','max_members','min_members','ratio','tag','done']
    column_exclude_list = ('description','have_extra_gems','extra_bids','required_gems')
    form_excluded_columns = ('participants','views','likes','plans','created','updated')
    form_widget_args = {
    'description': {
    'rows': 10,
    'style': 'color: black'
    }
    }
    def is_accessible(self):
        return checkAdmin('admin')


class AddressAdmin(ModelView):
    page_size = 30
    can_view_details = True
    form_excluded_columns = ('user','created','updated')

    def is_accessible(self):
        return checkAdmin('admin')

class StateAdmin(ModelView):
    page_size = 30
    can_view_details = True
    form_excluded_columns = ('created','updated')
    def is_accessible(self):
        return checkAdmin('admin')

class ExpireGiftField(SelectField):
    def __init__(self, *args, **kwargs):
        choices = [
            (False,'خیر'),
            (True,'بله')
        ]
        kwargs["choices"] = choices
        kwargs["coerce"] = lambda x: str(x) == "True"
        super(ExpireGiftField, self).__init__(*args, **kwargs)

class GiftAdmin(ModelView):
    form_overrides={
    'expired':ExpireGiftField
    }

    def is_accessible(self):
        return checkAdmin('admin')

class InsuranceAdmin(ModelView):
    def is_accessible(self):
        return checkAdmin('admin')

class GarantyAdmin(ModelView):
    def is_accessible(self):
        return checkAdmin('admin')

class InventoryAdmin(ModelView):
    def is_accessible(self):
        return checkAdmin('admin')

class ManufactureAdmin(ModelView):
    def is_accessible(self):
        return checkAdmin('admin')

class BidBooleanField(SelectField):
    def __init__(self, *args, **kwargs):
        choices = [
            (True, "برنده"),
            (False, "بازنده"),
        ]
        kwargs["choices"] = choices
        kwargs["coerce"] = lambda x: str(x) == "True"
        super(BidBooleanField, self).__init__(*args, **kwargs)

class BidAdmin(ModelView):
    form_overrides = {
        "won": BidBooleanField,
    }

    page_size = 30
    can_view_details = True
    column_searchable_list = ['user_plan.auction_plan.plan.title','user_plan.user.full_name','user_plan.user.username','auction.title','won']

    def is_accessible(self):
        return checkAdmin('admin')

class EventAdmin(ModelView):
    def is_accessible(self):
        return checkAdmin('admin')

class PaymentMethodAdmin(ModelView):
    def is_accessible(self):
        return checkAdmin('admin')

class ShipmentMethodAdmin(ModelView):
    page_size = 10
    can_view_details = True
    form_excluded_columns = ('created','updated')
    def is_accessible(self):
        return checkAdmin('admin')

class OrderAdmin(ModelView):
    form_choices = {
    'discount_status':[
    ('معمولی','معمولی'),
    ('شرکت کننده حراجی','شرکت کننده حراجی'),
    ('برنده حراجی','برنده حراجی'),
    ('منقضی شده','منقضی شده'),
    ],
    'status':[
    ('بدون پرداخت','بدون پرداخت'),
    ('درحال پرداخت','درحال پرداخت'),
    ('غیرفعال','غیرفعال'),
    ('پرداخت شده','پرداخت شده'),
    ]
    }

    page_size = 20
    can_view_details = True
    column_searchable_list = ['status','discount_status','item.title','item.product.title','user.full_name','user.username','payment.GUID','payment.status','payment.amount','payment.type']
    column_editable_list = ['status', 'discount_status','total']
    form_excluded_columns = ('created','updated')
    column_exclude_list = ('description')

    def is_accessible(self):
        return checkAdmin('admin')

class PaymentAdmin(ModelView):

    form_choices = {
    'status':[
    ('پرداخت موفق','پرداخت موفق'),
    ('درگاه بانک','درگاه بانک'),
    ('در حال پرداخت','در حال پرداخت'),
    ('خطا در پرداخت','خطا در پرداخت'),
    ('پرداخت لغو شده','پرداخت لغو شده'),
    ('پرداخت بایگانی شده','پرداخت بایگانی شده'),
    ('تلاش مجدد','تلاش مجدد'),
    ('پرداخت نشده','پرداخت نشده')
    ],
    'type':[
    ('اولیه','اولیه'),
    ('خرید مستقیم سکه حراجی','خرید مستقیم سکه حراجی'),
    ('خرید بسته الماس','خرید بسته الماس'),
    ('خرید محصول','خرید محصول'),
    ('خرید پکیج پیشنهادی','خرید پکیج پیشنهادی'),
    ('خرید رایگان','خرید رایگان')
    ]
    }

    page_size = 10
    can_view_details = True
    column_searchable_list = ['user.full_name','user.username','user.mobile','GUID','status','amount','type']
    column_editable_list = ['status','type']
    form_excluded_columns = ('user','created','updated')

    def is_accessible(self):
        return checkAdmin('admin')

class ShipmentAdmin(ModelView):

    form_choices = {
    'status':[
    ('سفارش داده شده','سفارش داده شده'),
    ('در انبار','در انبار'),
    ('آماده ارسال','آماده ارسال'),
    ('ارسال شده','ارسال شده'),
    ('تحویل داده شده','تحویل داده شده'),
    ]
    }
    page_size = 10
    can_view_details = True
    column_editable_list = ['status','send_date','recieve_date']
    column_searchable_list = ['guid','status','order.status','order.discount_status','order.item.title','order.item.product.title','order.user.full_name','order.user.username','order.payment.GUID','order.payment.status','order.payment.amount','order.payment.type','insurance.company']
    form_excluded_columns = ('created','updated','order','guid')

    def is_accessible(self):
        return checkAdmin('admin')

class PlanAdmin(ModelView):
    form_excluded_columns = ('created','updated')
    def is_accessible(self):
        return True
        return current_user.has_role('admin')

class UserPlanAdmin(ModelView):
    page_size = 20
    can_view_details = True
    column_searchable_list = ['user.full_name','user.username','auction_plan.plan.title']
    def is_accessible(self):
        return checkAdmin('admin')

class UserPlanPaymentAdmin(ModelView):
    page_size = 20
    can_view_details = True
    column_searchable_list = ['user_plan.user.full_name','user_plan.user.username','user_plan.auction_plan.plan.title']
    def is_accessible(self):
        return checkAdmin('admin')

class UserPlanCoinPaymentAdmin(ModelView):
    page_size = 20
    can_view_details = True
    column_searchable_list = ['user_plan.user.full_name','user_plan.user.username','user_plan.auction_plan.plan.title']
    def is_accessible(self):
        return checkAdmin('admin')

class UserPlanGemPaymentAdmin(ModelView):
    page_size = 20
    can_view_details = True
    column_searchable_list = ['user_plan.user.full_name','user_plan.user.username','user_plan.auction_plan.plan.title']

    def is_accessible(self):
        return checkAdmin('admin')

class AuctionPlanAdmin(ModelView):
    form_excluded_columns = ('created','updated')
    page_size = 10
    can_view_details = True
    column_searchable_list = ['auction.title','plan.title','needed_coins','max_bids','discount']
    def is_accessible(self):
        return checkAdmin('admin')

class UserAuctionParticipationAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['user.full_name','user.username','auction.title']
    def is_accessible(self):
        return checkAdmin('admin')

class UserMessageAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['title','subject','message','user.username','user.full_name']
    def is_accessible(self):
        return checkAdmin('admin')

class GuestMessageAdmin(ModelView):
    def is_accessible(self):
        return checkAdmin('admin')

class PaymentMessageAdmin(ModelView):
    page_size = 10
    can_view_details = True
    form_excluded_columns = ('updated','created')

    def is_accessible(self):
        return checkAdmin('admin')

class NotificationAdmin(ModelView):
    def is_accessible(self):
        return checkAdmin('admin')

class SiteNotificationAdmin(ModelView):
    form_choices = {
    'delivered':[
    (False, 'عدم تحویل'),
    (True, 'تحویل داده شده')],
    'seen':[
    (False, 'عدم مشاهده'),
    (True, 'مشاهده شده')],
    }

    page_size = 30
    can_view_details = True
    column_searchable_list = ['title','text','link','type','delivered','retry','user.username','user.mobile']
    column_editable_list = ['delivered','seen']
    form_excluded_columns = ('created','updated')
    def is_accessible(self):
        return checkAdmin('admin')

class UserNotificationAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['notification.text','notification.title','user.username','user.mobile']
    column_editable_list = ['delivered','seen','send_sms']
    def is_accessible(self):
        return checkAdmin('admin')

class AuctionNotificationAdmin(ModelView):
    def is_accessible(self):
        return checkAdmin('admin')

class UserAuctionNotificationAdmin(ModelView):
    page_size = 10
    can_view_details = True
    column_searchable_list = ['details','delivered','user.username','user.mobile','auction_notification.auction.title','auction_notification.text']
    column_editable_list = ['delivered','seen','details']
    def is_accessible(self):
        return checkAdmin('admin')

class SMSAdmin(ModelView):
    form_choices = {
    'delivered':[
    (False, 'عدم تحویل'),
    (True, 'تحویل داده شده')]
    }

    page_size = 10
    can_view_details = True
    column_searchable_list = ['delivered', 'status_code','text','title','user.username','user.mobile']
    column_editable_list = ['delivered']
    form_excluded_columns = ('created','updated')
    def is_accessible(self):
        return checkAdmin('admin')

class CreditLogAdmin(ModelView):
    page_size = 100
    can_view_details = True
    column_searchable_list = ['after_credit', 'before_credit','user.username','user.full_name','user.mobile']
    def is_accessible(self):
        return checkAdmin('admin')

class AvatarAdmin(ModelView):
    page_size = 20
    can_view_details = True
    form_excluded_columns = ('created','updated','users','chests')

    form_choices = {
    'type':[
    ('عمومی', 'عمومی'),
    ('اختصاصی', 'اختصاصی')],
    'color': [('bw', 'Black & White'), ('color', 'Color')]
    }


    def is_accessible(self):
        return checkAdmin('admin')

    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/avatars/" + form.thumbgen_filename(model.image).split("'")[1]))

        return Markup("<br />".join(gen_img(model.image) for image in ast.literal_eval(model.image)))

    column_formatters = {'image': _list_thumbnail}

    form_extra_fields = {'image': MultipleImageUploadField("Image",
                                                            base_path="project/static/images/avatars",
                                                            url_relative_path="images/avatars/",
                                                            thumbnail_size=(64, 64, 1))}

class UserAvatarAdmin(ModelView):
    def is_accessible(self):
        return checkAdmin('admin')

class UserGemAdmin(ModelView):
    def is_accessible(self):
        return checkAdmin('admin')

class UserCoinAdmin(ModelView):
    def is_accessible(self):
        return checkAdmin('admin')

class ActiveChestBooleanField(SelectField):
    def __init__(self, *args, **kwargs):
        choices = [
            (False,'پکیج غیرفعال'),
            (True,'نمایش پکیج در فروشگاه')
        ]
        kwargs["choices"] = choices
        kwargs["coerce"] = lambda x: str(x) == "True"
        super(ActiveChestBooleanField, self).__init__(*args, **kwargs)

class ChestAdmin(ModelView):
    page_size = 20
    can_view_details = True
    form_excluded_columns = ('created','updated')
    column_exclude_list = ('description')

    form_overrides ={
    'is_active':ActiveChestBooleanField,
    }

    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/chests/" + form.thumbgen_filename(model.image).split("'")[1]))

        return Markup("<br />".join(gen_img(model.image) for image in ast.literal_eval(model.image)))

    column_formatters = {'image': _list_thumbnail}

    form_extra_fields = {'image': MultipleImageUploadField("Image",
                                                            base_path="project/static/images/chests",
                                                            url_relative_path="images/chests/",
                                                            thumbnail_size=(64, 64, 1))}



    def is_accessible(self):
        return checkAdmin('admin')

class UserChestAdmin(ModelView):
    def is_accessible(self):
        return checkAdmin('admin')

class ActiveCharittyBooleanField(SelectField):
    def __init__(self, *args, **kwargs):
        choices = [
            (False,'خیریه غیرفعال'),
            (True,'خیریه فعال')
        ]
        kwargs["choices"] = choices
        kwargs["coerce"] = lambda x: str(x) == "True"
        super(ActiveCharittyBooleanField, self).__init__(*args, **kwargs)

class CharityAdmin(ModelView):
    page_size = 20
    can_view_details = True
    form_excluded_columns = ('created','updated')
    column_exclude_list = ('description')
    column_searchable_list = ['title','description']

    form_overrides={
    'is_active':ActiveCharittyBooleanField,
    }

    def _list_thumbnail(view, context, model, name):
        if not model.icon:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/charities/" + form.thumbgen_filename(model.icon).split("'")[1]))

        return Markup("<br />".join(gen_img(model.icon) for image in ast.literal_eval(model.icon)))

    column_formatters = {'icon': _list_thumbnail}

    form_extra_fields = {'icon': MultipleImageUploadField("Icon",
                                                            base_path="project/static/images/charities",
                                                            url_relative_path="images/charities/",
                                                            thumbnail_size=(64, 64, 1))}

    def is_accessible(self):
        return checkAdmin('admin')

class CoinAdmin(ModelView):
    page_size = 20
    can_view_details = True
    form_excluded_columns = ('created','updated')
    column_exclude_list = ('description')
    column_searchable_list = ['title','quantity','description','type']

    form_choices = {
    'type':[
    ('پیشنهادات روزانه', 'پیشنهادات روزانه'),
    ('بسته های فروشی', 'بسته های فروشی')],

    'color': [('bw', 'Black & White'), ('color', 'Color')]
    }

    def is_accessible(self):
        return checkAdmin('admin')

class GemAdmin(ModelView):
    page_size = 20
    can_view_details = True
    form_excluded_columns = ('created','updated')
    column_exclude_list = ('description')
    column_searchable_list = ['title','quantity','description','type']


    form_choices = {
    'type':[
    ('پیشنهادات روزانه', 'پیشنهادات روزانه'),
    ('بسته های فروشی', 'بسته های فروشی')],
    'color': [('bw', 'Black & White'), ('color', 'Color')]
    }

    def is_accessible(self):
        return checkAdmin('admin')

class GemPaymentAdmin(ModelView):
    page_size = 20
    can_view_details = True
    form_excluded_columns = ('user','created','updated')
    column_searchable_list = ['GUID','paid_gems','status','user.username','user.full_name','user.mobile']

    form_choices = {
    'type':[
    ('اولیه','اولیه'),
    ('تبدیل به سکه','تبدیل به سکه'),
    ('تبدیل به پلن حراجی','تبدیل به پلن حراجی'),
    ('تبدیل به آواتار','تبدیل به آواتار'),
    ('تبدیل به بید اضافه','تبدیل به بید اضافه')
    ],
    'status':[
    ('شکل گیری','شکل گیری'),
    ('منتظر تایید الماس','منتظر تایید الماس'),
    ('پرداخت الماس موفق','پرداخت الماس موفق'),
    ('همراه با خطا','همراه با خطا'),
    ('انجام شده','انجام شده')
    ]
    }

    def is_accessible(self):
        return checkAdmin('admin')

class CoinPaymentAdmin(ModelView):
    page_size = 20
    can_view_details = True
    form_excluded_columns = ('user','created','updated')
    column_searchable_list = ['GUID', 'paid_coins','status','user.username','user.full_name','user.mobile']

    form_choices = {
    'type':[
    ('اولیه','اولیه'),
    ('خرید پلن حراجی با موجودی سکه','خرید پلن حراجی با موجودی سکه'),
    ('شارژ کسری حساب الماس','شارژ کسری حساب الماس')
    ],
    'status':[
    ('شکل گیری','شکل گیری'),
    ('در حال محاسبه',' در حال محاسبه'),
    ('کسر از حساب موفق','کسر از حساب موفق'),
    ('همراه با خطا','همراه با خطا'),
    ('انجام شده','انجام شده')
    ]
    }

    def is_accessible(self):
        return checkAdmin('admin')

class LevelAdmin(ModelView):
    page_size = 20
    can_view_details = True
    form_excluded_columns = ('users','auctions','created','updated')
    column_exclude_list = ('description')
    column_searchable_list = ['title', 'number']


    def is_accessible(self):
        return checkAdmin('admin')

    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return None

        def gen_img(filename):
            return '<img src="{}">'.format(url_for('static',
                                                   filename="images/avatars/" + form.thumbgen_filename(model.image).split("'")[1]))

        return Markup("<br />".join(gen_img(model.image) for image in ast.literal_eval(model.image)))

    column_formatters = {'image': _list_thumbnail}

    form_extra_fields = {'image': MultipleImageUploadField("Images",
                                                            base_path="project/static/images/avatars",
                                                            url_relative_path="images/avatars/",
                                                            thumbnail_size=(64, 64, 1))}

class SettingAdmin(ModelView):
    page_size = 1
    can_view_details = True

    def is_accessible(self):
        return checkAdmin('admin')

class UserActivityAdmin(ModelView):
    page_size = 50
    can_view_details = True
    column_searchable_list = ['activity', 'ip','user.username','user.full_name','user.mobile']


    def is_accessible(self):
        return checkAdmin('admin')
