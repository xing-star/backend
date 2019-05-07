from functools import wraps
from flask import request, jsonify, g
from .models import Permission
from ..users.models import User


class HTTPPermission(object):

    def __init__(self):
        pass

    def permission_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_type, token = request.headers['Authorization'].split(
                'Bearer', 1)
            token = token.replace(" ", "")
            user = User.verify_auth_token(token)
            permission = Permission.query.filter(Permission.role_tags.like("%" + str(user.role_tag) + "%")).all()
            if not permission:
                return jsonify({
                    'status_code': '40021', 'error_message': 'Unauthorized Operation With Insufficient Permission'})
            for str_result in permission:
                if str_result.url in request.url:
                    return f(*args, **kwargs)
            return jsonify({
                'status_code': '40021', 'error_message': 'Unauthorized Operation With Insufficient Permission '})
        return decorated