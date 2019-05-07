from functools import wraps
from flask import request, jsonify, g
from ..users.models import User


class HTTPAuth(object):

    def __init__(self):
        pass

    def login_required(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if auth is None and 'Authorization' in request.headers:
                try:
                    auth_type, token = request.headers['Authorization'].split(
                        'Bearer', 1)
                    print(auth_type)
                    token = token.replace(" ", "")
                    user = User.verify_auth_token(token)
                    if not user:
                        return jsonify({'status_code': '40020', 'error_message': 'Unauthorized Operation With '
                                                                                 'Missing Or Incorrect Token'})
                    g.user=user
                    return f(*args, **kwargs)
                except ValueError:
                    pass
            return jsonify({'status_code': '40020', 'error_message': 'Unauthorized Operation With '
                                                                     'Missing Or Incorrect Token'})
        return decorated
