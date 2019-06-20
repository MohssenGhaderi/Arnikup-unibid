from project.database import db_session
from project import jwt
from project.model.user import User
from project.logger import Logger

class Jwt_helper:

    @staticmethod
    @jwt.user_loader_callback_loader
    def get_user(identity):
        session = db_session()
        return session.query(User).filter(User.username == identity).first()
