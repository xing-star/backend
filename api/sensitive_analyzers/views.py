from flask import request
from flask.views import MethodView
from .models import SensitiveAnalyzer
from flask import jsonify
from .. import http_auth, db
from datetime import datetime
from ..users.models import User


class ViewAll(MethodView):

    def __init__(self):
        pass

    @http_auth.login_required
    def get(self):
        try:
            result = SensitiveAnalyzer.query.all()
            result_set = []
            for result_model in result:
                user = User.query.filter_by(user_id=result_model.user_id).first()
                print(result_model.name)
                result_set.append(dict({"id": result_model.id, "name": result_model.name,
                                        "creator": user.name, "user_id": result_model.user_id,
                                        "created_at": result_model.created_at, "updated_at": result_model.updated_at}))
            return jsonify({
                            "sensitive_analyzers": result_set,
                            "status": {
                                "code": 200,
                                "is_error": False,
                                "message": "Successfully Retrieve All Users' Information"
                            }})
        except Exception as e:
            raise e


class ViewOne(MethodView):
    def __init__(self):
        self.id = request.args.get('id')

    @http_auth.login_required
    def get(self):
        try:
            result = SensitiveAnalyzer.query.filter_by(id=self.id, is_valid=True).first()
            if result:
                words_list = result.words.split("#")
                return jsonify({
                            "text_analyzer": {
                                "id": result.id,
                                "name": result.name,
                                "user_id": result.user_id,
                                "creator": result.user_name,
                                "target": result.target,
                                "words": words_list,
                                "created_at": result.created_at,
                                "updated_at": result.updated_at
                            },
                            "status": {
                                "code": 200,
                                "is_error": False,
                                "message": "Successfully Retrieve Certain Analyzer's Information"
                            }
                })
            else:
                return jsonify({
                    "status": {
                        "code": 40010,
                        "is_error": True,
                        "message": "Cannot Find Sensitive Analyzer With Given ID"


                    }
                })
        except Exception as e:
            raise e


class CreateSensitive(MethodView):

    def __init__(self):
        self.name = request.json.get("name")
        self.words = request.json.get("words")
        self.target = request.json.get("target")
        self.user_id = request.json.get("user_id")

    @http_auth.login_required
    def post(self):
        try:
            if self.name is None or self.words is None or self.target is None or self.user_id is None:
                return jsonify({
                        'status': {
                            "code": 40017,
                            "is_error": True,
                            "message": "Cannot Created Sensitive Because of the missing information"
                        }
                })
            result = SensitiveAnalyzer.query.filter_by(name=self.name, is_valid=True).first()
            if result:
                return jsonify({
                    'status': {
                        "code": 40011,
                        "is_error": True,
                        "message": "Cannot Create Sensitive Analyzer Because of Conflicted Name"
                    }
                })
            # 存入数据库中以#号分割
            str_words = '#'.join(self.words)
            sensitive = SensitiveAnalyzer(name=self.name, words=str_words, target=self.target)
            db.session.add(sensitive)
            db.session.commit()
            return jsonify({
                "sensitive_analyzer": {
                    "id": sensitive.id,
                    "name": sensitive.name,
                    "creator": g.user.user_id,
                    "user_id": sensitive.user_id,
                    "created_at": datetime.now,
                    "target": sensitive.target,
                    "words": self.words
                },
                "status": {
                    "code": 200,
                    "is_error": False,
                    "message": "Successfully Create Sensitive Analyzer"
                }
            })
        except Exception as e:
            raise e


class UpdateSensitive(MethodView):

    def __init__(self):
        self.id = request.args.get('id')
        self.name = request.json.get("name")
        self.words = request.json.get("words")
        self.target = request.json.get("target")
        self.user_id = request.json.get("user_id")

    @http_auth.login_required
    def put(self):
        try:
            if self.name is None and self.words is None and self.target is None or self.user_id is None:
                return jsonify({
                    "status": {
                        "code": 40017,
                        "is_error": True,
                        "message": "Cannot Update Sensitive Because of the missing information"

                    }
                })
            result = SensitiveAnalyzer.query.filter_by(id=self.id, is_valid=True).first()
            if result is None:
                return jsonify({
                    "status": {
                        "code": 40010,
                        "is_error": True,
                        "message": "Cannot Find Sensitive Analyzer With Given ID"

                    }
                })
            if self.name != result.name:
                exist_text = SensitiveAnalyzer.query.filter_by(id=self.id, is_valid=True).first()
                if exist_text:
                    return jsonify({
                        "status": {
                            "code": 40016,
                            "is_error": True,
                            "message": "Cannot Update Sensitive Because of the Conflicted Name"

                        }
                    })
            if self.name is not None and self.name != result.name:
                result.name = self.name
            if self.words is not None:
                str_words = '#'.join(self.words)
                result.words = str_words
            if self.target is not None and self.target != result.target:
                result.target = self.target
            if self.user_id is not None and self.target != result.user_id:
                result.user_id = self.user_id
            result.updated_at = datetime.now
            db.session.add(result)
            db.session.commit()
            return jsonify({
                "sensitive_analyzer": {
                    "id": self.id,
                    "name": self.name,
                    "creator": result.user_id,
                    "user_id": result.user_id,
                    "created_at": result.created_at,
                    "target": result.target,
                    "words": self.words
                },
                "status": {
                    "code": 200,
                    "is_error": False,
                    "message": "Successfully Update Sensitive Analyzer"
                }
            })
        except Exception as e:
            raise e


class DeleteSensitive(MethodView):

    def __init__(self):
        self.id = request.args.get('id')

    @http_auth.login_required
    def delete(self):
        try:
            result = SensitiveAnalyzer.query.filter_by(id=self.id, is_valid=True).first()
            if result is None:
                return jsonify({
                    "status": {
                        "code": 40010,
                        "is_error": True,
                        "message": "Cannot Find Sensitive Analyzer With Given ID"

                    }
                })
            # 伪删除处理
            result.is_valid = 0
            db.session.add(result)
            db.session.commit()
            return jsonify({
                "status": {
                    "code": 200,
                    "is_error": False,
                    "message": "Successfully Delete Sensitive Analyzer"
                }
            })
        except Exception as e:
            raise e

