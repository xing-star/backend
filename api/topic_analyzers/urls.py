from api import app
from api.topic_analyzers.views import ViewAll


def topic_analyzers_router():
    app.add_url_rule('/analyzers/topics/view', view_func=ViewAll.as_view('/analyzers/topics/view'), methods=['GET'])


