from .. import db
from .. import app
from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
import uuid


class User(db.Model):
    __tablename__ = 'users'

    def gen_id(self):
        return uuid.uuid4().hex

    id = db.Column(db.String(128), primary_key=True, default=gen_id)
    account = db.Column(db.String(64))
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    # 此处若命名为password会导致冲突发生，使得flask_migrate无法映射生成表结构
    pwd_hash = db.Column(db.String(128))
    role_tag = db.Column(db.Integer)
    # True为无效用户，False为有效用户
    is_valid = db.Column(db.Boolean, default=True)
    # 此处要修改成create_time
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now)

    def hash_password(self, password):
        self.pwd_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.pwd_hash)

    def generate_auth_token(self, expiration):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user
