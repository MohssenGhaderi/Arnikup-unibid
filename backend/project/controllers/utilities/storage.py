import os
from project import app
from project.database import db_session
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_current_user
from project.model.customer import Customer 
import definitions
from project.logger import Logger

class Storage:
    
    def __init__(self, username):
        self.username = username

    def get_user_dir(self):
        path = os.path.join(definitions.ROOT_DIR, 'storage' ,self.username)
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def save(self, file):
        pass

    def delete(self, file):
        pass

    
class Private_Storage(Storage):
    def __init__(self):
        user = get_current_user()
        Storage.__init__(self, user.username)

    def get_user_private_dir(self):
        return os.path.join(self.get_user_dir(), "private")

    def get_sheets_dir_for(self, exam_id):
        path = os.path.join(self.get_user_private_dir(), str(exam_id) , "sheets")
        if not os.path.exists(path):
            os.makedirs(path)
        return path

class Public_Storage(Storage):
    pass

class TEMP_Storage(Storage):

    def __init__(self):
        user = get_current_user()
        Storage.__init__(self, user.username)
    
    def get_user_temp_dir(self):
        return os.path.join(self.get_user_dir(), "temp")

    def get_png_temp_addr(self):
        path = self.get_user_temp_dir()
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def get_sheet_template_addr(self):
        path = os.path.join(definitions.STATIC_DIR, 'img', 'sheet_fa.tif')
        return path

