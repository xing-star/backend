# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_cors import CORS

db = SQLAlchemy()

config_name = config['default']

app = Flask(__name__)
app.config.from_object(config_name)
config_name.init_app(app)
db.init_app(app)

CORS(app)

# 初始化自定义装饰器，该装饰器用来验证用户请求是否带有合法token
from .auth.decorated import HTTPAuth
http_auth = HTTPAuth()
from .roles.decorated import HTTPPermission
http_permission = HTTPPermission()

from .auth.urls import auth_router
auth_router()
from .users.urls import user_router
user_router()
# from .text_analyzers.urls import text_analyzers_router
# text_analyzers_router()
from api.pattern_analyzers.urls import pattern_analyzers_router
pattern_analyzers_router()
# from api.sensitive_analyzers.urls import sensitive_analyzers_router
# sensitive_analyzers_router()

from api.topic_analyzers.urls import topic_analyzers_router
topic_analyzers_router()