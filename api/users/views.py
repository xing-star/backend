from flask import request
from flask.views import MethodView
from .models import User
from ..roles.models import Role
from flask import jsonify, g
from .. import http_auth, http_permission, db
from datetime import datetime
import re


class ViewAll(MethodView):

    def __init__(self):
        # 不判断是否非法，默认为第一页数据
        self.page = request.args.get('page', 1, type=int)

    @http_auth.login_required
    @http_permission.permission_required
    def get(self):
        try:
            """
            分页展示数据，self.page为前端传过来的当前页面数，
            per_page=1为每个页面展示的数据为一行（此处为方便测试展示一行，之后正式环境应改成每页展示10行数据）
            如果error_out为False则下列情况下不抛出404异常
            """
            per_page = 1
            user = User.query.filter_by(is_valid=True).paginate(self.page, per_page, error_out=False)
            total_page = user.pages
            result_set = []
            for items in user.items:
                role = Role.query.filter_by(tag=items.role_tag).first()
                result_set.append(dict({"user_id": items.id, "account": items.account,
                                      "name": items.name, "email": items.email,
                                      "role_tag": items.role_tag, "role_name": role.name,
                                      "created_at": items.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                      "updated_at": items.updated_at.strftime("%Y-%m-%d %H:%M:%S")}))
            return jsonify({
                            "users": result_set,
                            "status": {
                                "code": 200,
                                "is_error": False,
                                "message": "Successfully Retrieve All Users' Information"
                            },
                            "pages": {
                                "page": self.page,
                                "per_page": per_page,
                                "total_page": total_page
                            }
                })
        except Exception as e:
            raise e

        """
        未分页处理方法
        """
        # try:
        #     # 查询status为1，有效的用户。
        #     user = User.query.filter_by(status=1).all()
        #     result_set = []
        #     for user_model in user:
        #         result_set.append(dict({"id": user_model.id, "user_id": user_model.user_id,
        #                               "name": user_model.name, "email": user_model.email,
        #                               "role": user_model.role, "created_at": user_model.created_at}))
        #     return jsonify({
        #                     "users": result_set,
        #                     "status": {
        #                         "code": 200,
        #                         "is_error": False,
        #                         "message": "Successfully Retrieve All Users' Information"
        #                     }})
        # except Exception as e:
        #     raise e


class ViewOne(MethodView):

    def __init__(self):
        self.id = request.args.get('id')

    @http_auth.login_required
    @http_permission.permission_required
    def get(self):
        try:
            result = User.query.filter_by(id=self.id).first()
            if result:
                role = Role.query.filter_by(tag=result.role_tag).first()
                return jsonify({
                    "user": {
                        "id": result.id,
                        "account": result.account,
                        "name": result.name,
                        "email": result.email,
                        # 此处role_name还是需要返回id，并返回角色id对应的名字
                        "role_tag": result.role_tag,
                        "role_name": role.name,
                        "created_at": result.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "updated_at": result.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                    },
                    "status": {
                        "code": 200,
                        "is_error": False,
                        "message": "Successfully Retrieve Certain User's Information"
                    }
                })
            else:
                return jsonify({
                    "status": {
                        "code": 40001,
                        "is_error": True,
                        "message": "Cannot Find User With Given User ID %s" % self.id


                    }
                })
        except Exception as e:
            raise e


class CreateUser(MethodView):

    def __init__(self):
        print(request.get_data())
        print(request.get_json())
        self.account = request.json.get('account')
        self.password = request.json.get('password')
        self.name = request.json.get('name')
        self.email = request.json.get('email')
        self.role_tag = request.json.get('role_tag')

    @http_auth.login_required # 为方便创建用户暂时不添加登录验证
    @http_permission.permission_required
    def post(self):
        try:
            if self.account is None or self.password is None or self.name is None or self.role_tag is None:
                return jsonify({
                    'status': {
                        "code": 40004,
                        "is_error": True,
                        "message": "Cannot Create User Because of the missing information"
                    }
                })
            # 正则表达式-后续完成
            # result_email = re.compile(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$')
            # # result_tag = re.compile(r'[0-10]')
            # result_password = re.compile(r'^(?=.* \d)(?=.*[a - z])(?=.*[A-Z]).{8, 10}$')
            #
            # if result_password.match(self.password) is False:
            #     print("-------")
            # else:
            #     print("+++++++")
            # if result_email.match(self.email) is False:
            #     print("-------")
            # else:
            #     print("+++++++")

            # result_password = re.compile(r'^[a-zA-Z]\w{6,18}')
            # result_email = re.compile(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$')
            # result_tag = re.compile(r'[0-10]')
            # if result_password.match(self.password):
            #     print("success")
            # else:
            #     print("fail")
            #     return "fail"
            # if 1 > len(self.account) > 20 or result_password.match(self.password) is False or 1 > len(
            #         self.name) > 20 or result_email.match(self.email) is False or result_tag.match(self.role_tag
            #         ) is False:
            #     return jsonify({
            #         'status': {
            #             "code": 40008,
            #             "is_error": True,
            #             "message": "Cannot Update User Because of the Illegal Information"
            #         }
            #     })
            if User.query.filter_by(account=self.account, is_valid=True).first() is not None:
                return jsonify({
                        'status': {
                            "code": 40002,
                            "is_error": True,
                            "message": "Cannot Create User Because Of Repeated User ID %s" % self.account
                        }
                })  # existing user
            user = User(account=self.account, name=self.name, email=self.email, role_tag=self.role_tag)
            user.hash_password(self.password)
            role = Role.query.filter_by(tag=self.role_tag).first()
            if role is None:
                return jsonify({
                    "status": {
                        "code": 40005,  # 代码需要更改
                        "is_error": True,
                        "message": "Cannot Create User Because of the Illegal Information"
                    }
                })
            db.session.add(user)
            db.session.commit()
            return jsonify({
                "user": {
                    "id": user.id,
                    "account": user.account,
                    "name": user.name,
                    "email": user.email,
                    "role_tag": user.role_tag,
                    "role_name": role.name,
                    "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                },
                "status": {
                    "code": 200,
                    "is_error": False,
                    "message": "Successfully Created A New User"
                }
            })
        except Exception as e:
            raise e


class DeleteUser(MethodView):

    def __init__(self):
        self.id = request.args.get('id')

    @http_auth.login_required
    @http_permission.permission_required
    def delete(self):
        try:
            result = User.query.filter_by(id=self.id).first()

            if result:
                if g.user.id == self.id:
                    return jsonify({
                        "status": {
                            "code": 40001,# 代码需要更改
                            "is_error": True,
                            "message": "Cannot delete yourself"
                        }
                    })
                result.is_valid = 0
                db.session.add(result)
                db.session.commit()
                return jsonify({
                    "status": {
                        "code": 200,
                        "is_error": False,
                        "message": "Successfully Deleted Certain User"
                    }
                })
            return jsonify({
                "status": {
                    "code": 40006,
                    "is_error": True,
                    "message": "Cannot Delete User With Given ID"  # 无法找到用户用给出的ID
                }
            })
        except Exception as e:
            raise e


class UpdateUser(MethodView):

    def __init__(self):
        self.id = request.args.get('id')
        self.account = request.json.get('account')
        self.password = request.json.get('password')
        self.name = request.json.get('name')
        self.email = request.json.get('email')
        self.role_tag = request.json.get('role_tag')

    @http_auth.login_required
    @http_permission.permission_required
    def put(self):
        exist_user = ""
        try:
            result = User.query.filter_by(id=self.id, is_valid=True).first()
            if g.user.account != self.account:
                exist_user = User.query.filter_by(account=self.account, is_valid=True).first()

            if result is None:
                return jsonify({
                    "status": {
                        "code": 40007,
                        "is_error": True,
                        "message": "Cannot Update User With Given ID"  # 无法用给出的ID找到对应的用户
                    }
                })

            # 修改的时候账号不可以是从数据库里面查询出来的账号
            if exist_user:
                return jsonify({
                    "status": {
                        "code": 40009,
                        "is_error": True,
                        "message": "Cannot Update User Because of the Conflicted Account"  # 因为重复的UserID不能更新用户
                    }
                })
            if self.account is None and self.name is None and \
                self.email is None and self.role_tag is None and self.password is None:
                return jsonify({
                    "status": {
                        "code": 40008,
                        "is_error": True,
                        "message": "Cannot Update User Because of the Illegal Information"
                    }
                })
            if self.account is not None:
                if User.query.filter_by(account=self.account, is_valid=True).first() is not None:
                    return jsonify({
                        'status': {
                            "code": 40009,
                            "is_error": True,
                            "message": "Cannot Update User Because of the Conflicted Account"
                        }
                    })
                result.account = self.account
            if self.name is not None:
                result.name = self.name
            if self.email is not None:
                result.email = self.email
            if self.role_tag is not None:
                result.role_tag = self.role_tag
            result.updated_at = datetime.now()
            if self.password is not None:
                # 管理员修改用户密码无需校验旧密码
                result.hash_password(self.password)
            db.session.add(result)
            db.session.commit()
            return jsonify({
                "updated_user": {
                    "id": self.id,
                    "account": self.account,
                    "name": self.name,
                    "email": self.email,
                    "role_tag": self.role_tag,
                    "created_at": result.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": result.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                },
                "status": {
                    "code": 200,
                    "is_error": False,
                    "message": "Successfully update the User"
                }
            })
        except Exception as e:
            raise e


class UpdatePassword(MethodView):

    def __init__(self):
        self.id = request.args.get('id')
        self.old_password = request.json.get('old_password')
        self.new_password = request.json.get('new_password')

    @http_auth.login_required
    def put(self):
        try:
            if self.id is None or self.old_password is None or self.new_password is None:
                return jsonify({
                    'status': {
                        "code": 40013,
                        "is_error": True,
                        "message": "Cannot Update Password Because of the missing information"
                    }
                })
            result = User.query.filter_by(id=self.id).first()
            if result.verify_password(self.old_password) is False:
                return jsonify({
                    'status': {
                        "code": 40014,
                        "is_error": True,
                        "message": "Cannot Update Password Because of the Password is Error"
                    }
                })
            if self.old_password == self.new_password:
                return jsonify({
                    'status': {
                        "code": 40015,
                        "is_error": True,
                        "message": "Cannot Update Password Because of Conflicted Password"
                    }
                })

            result.hash_password(self.new_password)
            result.updated_at = datetime.now()
            db.session.add(result)
            db.session.commit()
            return jsonify({
                "updated_password": {
                    "id": self.id,
                    "account": result.account,
                    "name": result.name,
                    "email": result.email,
                    "role_tag": result.role_tag,
                    "created_at": result.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at": result.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                },
                "status": {
                    "code": 200,
                    "is_error": False,
                    "message": "Successfully update the Password"
                }
            })
        except Exception as e:
            raise e
