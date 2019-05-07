import os
from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView

from .. import db, http_auth
from api.topic_analyzers.models import TopicModel

class ViewAll(MethodView):

    def __init__(self):
        pass

    # @http_auth.login_required
    def get(self):
        pass