from .. import db
import uuid
from datetime import datetime


class TopicModel(db.Model):
    __tablename__ = 'topics'

    def gen_id(self):
        return uuid.uuid4().hex

    id = db.Column(db.String(128), primary_key=True, default=gen_id)
    name = db.Column("name", db.String(64))
    description = db.Column("description", db.Text)
    is_valid = db.Column('is_valid', db.Boolean, default=True)
    user_id = db.Column('user_id', db.String(128), db.ForeignKey('users.id'))
    created_at = db.Column('created_at', db.DateTime(), default=datetime.now)
    updated_at = db.Column('updated_at', db.DateTime(), default=datetime.now)