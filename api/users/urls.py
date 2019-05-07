from .. import app
from .views import *


def user_router():
    app.add_url_rule('/users/view', view_func=ViewAll.as_view('/users/view'), methods=['GET'])
    app.add_url_rule('/users/one', view_func=ViewOne.as_view('/users/one'), methods=['GET'])
    app.add_url_rule('/users/create', view_func=CreateUser.as_view('/users/create'), methods=['POST'])
    app.add_url_rule('/users/delete', view_func=DeleteUser.as_view('/users/delete'), methods=['DELETE'])
    app.add_url_rule('/users/update', view_func=UpdateUser.as_view('/users/update'), methods=['PUT'])
    app.add_url_rule('/users/password', view_func=UpdatePassword.as_view('/users/password'), methods=['PUT'])
