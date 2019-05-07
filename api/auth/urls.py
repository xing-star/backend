from .. import app
from .views import Login


def auth_router():
    app.add_url_rule('/auth/login', view_func=Login.as_view('/auth/login'))