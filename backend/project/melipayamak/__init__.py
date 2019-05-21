from .melipayamak import SMS_Api
from definitions import SMS_USERNAME,SMS_PASSWORD,SMS_SERVICE_NUMBER
from project.model import UserSMS
from project.database import db

sms_api = SMS_Api(SMS_USERNAME,SMS_PASSWORD)
sms = sms_api.sms()

def SendMessage(user,title,message,text,bodyId):

    try:
        print ("sending sms to ",user.mobile)
        resp = sms.send(user.mobile ,SMS_SERVICE_NUMBER,message)
        result = {"status_code":resp['Value']}
        if resp['RetStatus'] == 1 and len(resp['Value'])>15 and resp['StrRetStatus']== 'Ok' :
            result["success"] = True
        else:
            result["success"] = False
            resp = sms.send_force(SMS_SERVICE_NUMBER,user.mobile, text, bodyId)
            result = {"status_code":resp['Value']}
            if resp['RetStatus'] == 1 and len(resp['Value'])>15 and resp['StrRetStatus']== 'Ok' :
                result["success"] = True
            else:
                result["success"] = False

        user_sms = UserSMS()
        user_sms.title = title
        user_sms.text = message
        user_sms.user = user
        user_sms.status_code = int(result['status_code'])
        user_sms.delivered = result['success']
        db.session.add(user_sms)
        db.session.commit()
        return result
    except Exception as e:
        return {"status_code":-100,"success":False}

def SendSMS(mobile,message):
    print ("sending sms to ",mobile)
    sms_api = SMS_Api(SMS_USERNAME,SMS_PASSWORD)
    sms = sms_api.sms()
    resp = sms.send(mobile ,SMS_SERVICE_NUMBER,message)
    print ("response",resp)
    result = {"status_code":resp['Value']}
    if resp['RetStatus'] == 1 and len(resp['Value'])>15 and resp['StrRetStatus']== 'Ok' :
        result["success"] = True
    else:
        result["success"] = False
    return result

def SendSMSForce(mobile,text,bodyId):
    print ("send force sms to ",mobile)
    sms_api = SMS_Api(SMS_USERNAME,SMS_PASSWORD)
    sms = sms_api.sms()
    resp = sms.send_force(SMS_SERVICE_NUMBER,mobile, text, bodyId)
    print ("response",resp)
    result = {"status_code":resp['Value']}

    if resp['RetStatus'] == 1 and len(resp['Value'])>15 and resp['StrRetStatus']== 'Ok' :
        result["success"] = True
    else:
        result["success"] = False
    return result
