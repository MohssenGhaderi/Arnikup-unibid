import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is Project Root
STATIC_DIR = os.path.join(ROOT_DIR, "project/static/")
AVATAR_DIR = os.path.join(ROOT_DIR, "project/files/avatars")
PRODUCT_IMAGE_PATH = "/static/images/products/"

BASE_BID_PRICE = 1000
BASE_USER_CREDIT = 0
SESSION_EXPIRE_TIME = 365
UPLOAD_FOLDER = os.path.join(STATIC_DIR, 'messages', 'attachments')
ALLOWED_EXTENTIONS = set(['text', 'pdf', 'doc', 'docs', 'jpg', 'jpeg', 'png'])
MESSAGE_SUBJECTS = [{"title":'درخواست کمک','type':1},{"title":'مشکل در سایت','type':2},{"title":'تقدیر و تشکر','type':3}]

#bank
BANK_MELLAT_TERMINAL_ID = 3556904
BANK_MELLAT_USERNAME = "bid2172"
BANK_MELLAT_PASSWORD = 49413744
MAXIMUM_ORDERS = 3
MAX_SEARCH_RESULT = 10
COUPONCODE = "ipuw-01mljeifb090[1n24p9[kjnqk]]"

SMS_SERVICE_NUMBER = '500010601642'
SMS_USERNAME = '09017414372'
SMS_PASSWORD = '3469'

SMS_BodyId_VER = 2982
SMS_BodyId_WEL = 2161
SMS_BodyId_FPS = 2162
SMS_BodyId_CHPS = 2163
SMS_BodyId_GIFT_INVITOR = 2182
SMS_BodyId_GIFT_USER = 2184

# SITE_PREFIX = "https://unibid.ir"
SITE_PREFIX = "https://unibid.ir"


# CALLBACKLINK = "http://127.0.0.1:4200/v2/api/payment/zarinpal/callback"
CALLBACKLINK = "https://admin.unibid.ir/v2/api/payment/zarinpal/callback"

MAX_SMS_RETRY = 1

MAX_ACTIVATION_ATTEMPTS = 3
MAX_LOGIN_ATTEMPTS = 20
MAX_MESSAGES_SEND = 5
MAX_DEFFER_ACTIVATION_TIME = 30 * 60
MAX_AVAILABLE_MESSAGE_TIME = 120
MAX_INVITOR_POLICY = 5
MAX_MESSAGE_POLICY = 10

COINS_BASE_PRICE = 1000
GEMS_BASE_PRICE = 20000
AUCTION_START_DEADLINE = 60
AUCTION_START_PROGRESS = 60
AUCTION_WINNER_POINT_FRACTION = 20
