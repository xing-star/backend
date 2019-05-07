from flask import request
from flask.views import MethodView
from ..users.models import User
from flask import jsonify
import datetime
from ..roles.models import Permission, Role


class Login(MethodView):

    def __init__(self):
        self.account = request.json.get('account')
        self.password = request.json.get("password")

    def post(self):
        try:
            result = User.query.filter_by(account=self.account).first()
            if result is not None and result.is_valid is False:
                return jsonify({
                    "status": {
                        "code": 40003,
                        "is_error": True,
                        "message": "Cannot Login User Because the given user has been suspended or deleted"
                    }
                })
            if result is not None and result.verify_password(self.password):
                role = Role.query.filter_by(tag=result.role_tag).first()
                permission = Permission.query.filter(Permission.role_tags.like("%"+str(result.role_tag)+"%")).all()
                url_list = []
                for str_result in permission:
                    url_list.append(str_result.module)
                # 去重后成为一个set值，set值不支持json，再包装成list
                url_list = list(set(url_list))
                token = result.generate_auth_token(21600)  # 此处为了方便前端的测试改成60秒之后需要改成600秒
                expire_date = (datetime.datetime.now() + datetime.timedelta(hours=6)).strftime("%Y-%m-%d %H:%M:%S")
                return jsonify({
                        "user_id": result.id,
                        "token": token.decode('ascii'),
                        "expire_at": expire_date,
                        "permitted_modules": url_list,
                        "account": result.account,
                        "name": result.name,
                        "email": result.email,
                        "status": {
                            "code": 200,
                            "is_error": False,
                            "message": "Successfully Retrieve All Users' Information"
                        },
                        "roles": {
                            "role_tag": result.role_tag,
                            "name": role.name
                        }

                    })
            return jsonify({
                    "status": {
                        "code": 40000,
                        "is_error": True,
                        "message": "Cannot Login User With Given Username And Password"
                    }
                })
        except Exception as e:
            raise e