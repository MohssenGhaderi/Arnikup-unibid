from flask_restful import Resource
from .Payment.Zarinpal import ZarinpalPaymentAPI
from flask_login import login_required, current_user
from flask import make_response, jsonify, url_for, request, render_template ,redirect
from definitions import BANK_MELLAT_PASSWORD, BANK_MELLAT_TERMINAL_ID, BANK_MELLAT_USERNAME
import random
from ..model.payment import *
from ..model.order import *
from ..model.user import *
import time
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, fresh_jwt_required

class ZarinpalGateway(Resource):
    @jwt_required
    def post(self):
        data = request.get_json(force=True)
        pid = int(data.get("pid", None))
        payment = Payment.query.get(pid)
        orders = Order.query.filter_by(payment_id = pid).all()
        for order in orders:
            order.status = OrderStatus.DEACTIVATE
            db.session.add(order)
            db.session.commit()

        zpl = ZarinpalPaymentAPI()
        pay_token = zpl.send_request(int(payment.amount),current_user.email,current_user.mobile,"http://unibid.ir/api/user/zarinpal/gateway/callback" ,"درگاه پرداخت یونی بید")
        payment.ref_id = pay_token.Authority
        payment.status = PaymentStatus.BANK
        db.session.add(payment)
        db.session.commit()
        print ('pid',pid,'token',pay_token)
        if pay_token.Status==100:
            return make_response(jsonify({'success':True,"ref_id": pay_token.Authority}), 200)
        else:
            return make_response(jsonify({'success':False,"ref_id": pay_token.Authority,"message":"خطای پرداخت"}),400)


class ZarinpalGatewayCallback(Resource):
    def get(self):
        status = request.args.get('Status')
        authority = request.args.get('Authority')

        payment = Payment.query.filter_by(ref_id=authority).first()

        zpl = ZarinpalPaymentAPI()
        verify_res = zpl.verify(status,authority,payment.amount)
        print ('verify_res',verify_res)
        if verify_res == 100:
            payment.status = PaymentStatus.PAID
        elif(verify_res == -21 or verify_res == -22):
            payment.status = PaymentStatus.ABORT
        else:
            payment.status = PaymentStatus.UNPAID

        db.session.add(payment)
        db.session.commit()

        return redirect('/callback/payment/'+str(payment.id))
