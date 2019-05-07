from .. import db
import uuid
from datetime import datetime


class PatternAnalyzerModel(db.Model):
    __tablename__ = 'pattern_analyzers'

    def gen_id(self):
        return uuid.uuid4().hex

    id = db.Column(db.String(128), primary_key=True, default=gen_id)
    name = db.Column("name", db.String(64))
    description = db.Column("description", db.Text)
    target = db.Column('target', db.Integer, default=0)
    is_valid = db.Column('is_valid', db.Boolean, default=True)
    user_id = db.Column('user_id', db.String(128), db.ForeignKey('users.id'))
    topic_id = db.Column('topic_id', db.String(128), db.ForeignKey('topics.id'))
    created_at = db.Column('created_at', db.DateTime(), default=datetime.now)
    updated_at = db.Column('updated_at', db.DateTime(), default=datetime.now)


class PatternNodesModel(db.Model):
    __tablename__ = 'pattern_nodes'

    def gen_id(self):
        return uuid.uuid4().hex
    id = db.Column(db.String(128), primary_key=True, default=gen_id)
    name = db.Column(db.String(64))
    description = db.Column(db.String(64))
    pattern_analyzer_id = db.Column('pattern_analyzer_id', db.String(128), db.ForeignKey('pattern_analyzers.id'))
    keywords = db.Column(db.Text)
    sentences = db.Column(db.Text)
    user_id = db.Column('user_id', db.String(128), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now)
    is_valid = db.Column(db.Boolean, default=True)
