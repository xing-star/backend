from .. import db
import uuid
from datetime import datetime


class SensitiveAnalyzer(db.Model):
    __tablename__ = 'sensitive_analyzer'

    def gen_id(self):
        return uuid.uuid4().hex
    id = db.Column(db.String(128), primary_key=True, default=gen_id)
    # 其中此处存role_ids 存储是已逗号隔开的roles (用0-10的整数)
    name = db.Column(db.String(64))
    is_valid = db.Column(db.Boolean, default=True)
    # 相似词以#分割开来
    words = db.Column(db.Text)
    # 文本分析器分析对象, 0表示所有对象，1表示仅对话务员，2表示仅对客户
    target = db.Column(db.Integer)
    user_id = db.Column(db.String(128))
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now)