
import datetime

from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id =db.Column(db.String(50),unique = True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True,nullable=False)
    password = db.Column(db.String(128))
    admin = db.Column(db.Boolean)
    custid = db.Column(db.String(64),nullable=False) # Same as tenantID -- it is used for tenant Management
    deleted = db.Column(db.Boolean)
    created_on = db.Column(db.DateTime, nullable=False)


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.utcnow()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False