from .. import app
from .views import *


def text_analyzers_router():
    app.add_url_rule('/analyzers/text/view', view_func=ViewAll.as_view('/analyzers/text/view'), methods=['GET'])
    app.add_url_rule('/analyzers/text/one', view_func=ViewOne.as_view('/analyzers/text/one'), methods=['GET'])
    app.add_url_rule('/analyzers/text/create', view_func=CreateText.as_view('/analyzers/text/create'), methods=['POST'])
    app.add_url_rule('/analyzers/text/update', view_func=UpdateText.as_view('/analyzers/text/update'), methods=['PUT'])
    app.add_url_rule('/analyzers/text/delete', view_func=DeleteText.as_view('/analyzers/text/delete'), methods=['DELETE'])

