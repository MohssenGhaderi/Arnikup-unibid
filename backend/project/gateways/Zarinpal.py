from flask import Flask, url_for, redirect, request
from suds.client import Client

class ZarinpalPaymentAPI(object):
    """
    docstring for ZarinpalPaymentAPI
    @param merchent_id: terminal merchent id
    @return: None
    """

    # MMERCHANT_ID = '7ac2e0d0-c7a0-11e8-a5d9-005056a205be'  # pooria
    # MMERCHANT_ID = 'ca35c8ec-3cc8-11e9-a358-005056a205be'  # soori
    MMERCHANT_ID = 'beff68ea-3be5-11e9-98b5-005056a205be'
    ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
    # ZARINPAL_WEBSERVICE = 'https://sandbox.zarinpal.com/pg/services/WebGate/wsdl'  # Required

    def send_request(self,amount,email,mobile,verify_url,description):
        print (verify_url)

        from suds.client import Client

        client = Client(self.ZARINPAL_WEBSERVICE)
        result = client.service.PaymentRequest(self.MMERCHANT_ID,amount,description,email,mobile,verify_url)
        print (result)
        return result
        # if result.Status == 100:
        #     return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
        # else:
        #     return 'Error'

    def verify(self,status,authority,amount):
        client = Client(self.ZARINPAL_WEBSERVICE)
        result = client.service.PaymentVerification(self.MMERCHANT_ID,authority,amount)
        return result.Status

        #     if result.Status == 100:
        #         return 'Transaction success. RefID: ' + str(result.RefID)
        #     elif result.Status == 101:
        #         return 'Transaction submitted : ' + str(result.Status)
        #     else:
        #         return 'Transaction failed. Status: ' + str(result.Status)
        # else:
        #     return 'Transaction failed or canceled by user'
