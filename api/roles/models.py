from .. import db
import uuid


class Permission(db.Model):
    __tablename__ = 'permissions'

    def gen_id(self):
        return uuid.uuid4().hex

    id = db.Column(db.String(128), primary_key=True, default=gen_id)
    # 其中此处存role_ids 存储是已逗号隔开的roles (用0-10的整数)
    role_tags = db.Column(db.String(64))
    url = db.Column(db.String(64))
    method = db.Column(db.String(64))
    description = db.Column(db.Text)
    # 前端对应的大的模组
    module = db.Column(db.String(64))


class Role(db.Model):
    __tablename__ = 'roles'

    def gen_id(self):
        return uuid.uuid4().hex
    id = db.Column(db.String(128), primary_key=True, default=gen_id)
    tag = db.Column(db.Integer)
    name = db.Column(db.String(64))