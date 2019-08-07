from ..model import *
from flask_restplus import Resource, fields, Namespace
from flask import url_for, redirect, request, abort, make_response , jsonify , session, flash
from project import app, rest_api
from datetime import datetime
from sqlalchemy import or_, asc, desc
from ..model.guest_message import GuestMessage
from project.utils import token_required, token_optional
from project.helpers import *
from project.lang.fa import *
from definitions import SITE_PREFIX, COINS_BASE_PRICE, GEMS_BASE_PRICE, CALLBACKLINK
import math
from project.gateways.Zarinpal import ZarinpalPaymentAPI

payment_ns = Namespace('payment')

payment_fields = payment_ns.model('PaymentModel', {
    "GUID":fields.String()
})

@payment_ns.route('/zarinpal/gateway')
class ZarinpalGateway(Resource):
    parser = rest_api.parser()
    parser.add_argument('Authorization',type=str,location='headers',help='Bearer Access Token (using example: "Bearer token")',required=True)
    @payment_ns.header('Authorization: Bearer', 'JWT TOKEN', required=True)
    @payment_ns.doc('buy chest api.', parser=parser, body=payment_fields, validate=True)
    @payment_ns.response(200, 'Success')
    @token_required
    def post(self,current_user):
        if 'GUID' not in payment_ns.payload:
            return make_response(jsonify({"success":False,"reason":"GUID","message":PAYMENT['GUID']}),400)

        result = Payment.query.filter_by(GUID=payment_ns.payload['GUID'])

        if result.count() > 1 :
            return make_response(jsonify({"success":False,"reason":"reapetedGUID","message":PAYMENT['REAPETED']}),403)

        if not result.first():
            return make_response(jsonify({"success":False,"reason":"paymentNotFound","message":PAYMENT['NOT_FOUND']}),400)

        payment = result.first()

        zpl = ZarinpalPaymentAPI()
        pay_token = zpl.send_request(int(payment.amount),current_user.email,current_user.mobile, CALLBACKLINK ,"درگاه پرداخت یونی بید")

        if pay_token.Status==100:
            payment.reference_id = pay_token.Authority
            payment.status = PaymentStatus.BANK
            db.session.add(payment)
            db.session.commit()
            return make_response(jsonify({"success":True,"message":PAYMENT['SUCCESS'],"authority":pay_token.Authority}),200)
        else:
            payment.reference_id = pay_token.Authority
            payment.status = PaymentStatus.RETRY
            db.session.add(payment)
            db.session.commit()
            return make_response(jsonify({"success":False,"reason":"authority","message":PAYMENT['AUTORITY']}),403)


@payment_ns.route('/zarinpal/callback')
class ZarinpalCallback(Resource):
    def get(self):
        status = request.args.get('Status')
        authority = request.args.get('Authority')

        payment = Payment.query.filter_by(reference_id=authority).first()

        zpl = ZarinpalPaymentAPI()
        verify_res = zpl.verify(status,authority,payment.amount)
        print(verify_res)
        
        if verify_res == 100:
            payment.status = PaymentStatus.PAID
        elif(verify_res == -21 or verify_res == -22):
            payment.status = PaymentStatus.ABORT
        else:
            payment.status = PaymentStatus.UNPAID

        db.session.add(payment)
        db.session.commit()
        return redirect('https://unibid.ir/')
