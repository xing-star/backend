from .. import app
from .views import *


def pattern_analyzers_router():
    app.add_url_rule('/analyzers/patterns/view', view_func=ViewAll.as_view('/analyzers/patterns/view'), methods=['GET'])
    app.add_url_rule('/analyzers/patterns/one', view_func=ViewOne.as_view('/analyzers/patterns/one'), methods=['GET'])
    app.add_url_rule('/analyzers/patterns/create', view_func=CreatePattern.as_view('/analyzers/patterns/create'), methods=['POST'])
    app.add_url_rule('/analyzers/pattern/update/node/new', view_func=UpdateNodeNew.as_view(
        '/analyzers/pattern/update/node/new'), methods=['PUT'])
    app.add_url_rule('/analyzers/pattern/update/node/update', view_func=UpdateNodeUpdate.as_view(
        '/analyzers/pattern/update/node/update'), methods=['PUT'])
    app.add_url_rule('/analyzers/pattern/update/node/delete', view_func=UpdateNodeDelete.as_view(
        '/analyzers/pattern/update/node/delete'), methods=['PUT'])
    app.add_url_rule('/analyzers/pattern/delete', view_func=DeletePattern.as_view(
        '/analyzers/pattern/delete'), methods=['DELETE'])

