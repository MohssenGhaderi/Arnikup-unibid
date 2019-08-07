import gevent
from gevent import monkey
monkey.patch_all()
import os
import logging
from project import app, socketio
from project.database import *
from project.admin import admin
import time
import datetime
from project.model import *
from definitions import MAX_SMS_RETRY,SITE_PREFIX
from project.melipayamak import SendMessage

if __name__ == '__main__':

    # production
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.DEBUG)
    logging.getLogger('suds.transport').setLevel(logging.DEBUG)

    port = int(os.environ.get("PORT", 8000))
    app.debug = False
    applogger = app.logger
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)
    applogger.setLevel(logging.DEBUG)
    applogger.addHandler(file_handler)
    socketio.run(app, port=port, debug=False,keyfile='ssl/admin.unibid.ir.key', certfile='ssl/admin.bundle.cer')


    # developement
    # port = int(os.environ.get("PORT", 9001))
    # app.debug = True
    # socketio.run(app, port=port, debug=True)
