from project.database import db, Base

class Revoked(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.BigInteger, primary_key = True)
    jti = db.Column(db.String(255))

    def add(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)
