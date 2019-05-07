from .. import app
from .views import *


def sensitive_analyzers_router():
    app.add_url_rule('/analyzers/sensitive/view', view_func=ViewAll.as_view('/analyzers/sensitive/view'), methods=['GET'])
    app.add_url_rule('/analyzers/sensitive/one', view_func=ViewOne.as_view('/analyzers/sensitive/one'), methods=['GET'])
    app.add_url_rule('/analyzers/sensitive/create', view_func=CreateSensitive.as_view('/analyzers/sensitive/create'
                                                                                      ), methods=['POST'])
    app.add_url_rule('/analyzers/sensitive/update', view_func=UpdateSensitive.as_view('/analyzers/sensitive/update'
                                                                                      ), methods=['PUT'])
    app.add_url_rule('/analyzers/sensitive/delete', view_func=DeleteSensitive.as_view('/analyzers/sensitive/delete'
                                                                                      ), methods=['DELETE'])

