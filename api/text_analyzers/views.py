from flask import request
from flask.views import MethodView
from .models import TextAnalyzer
from flask import jsonify
from .. import http_auth, db
from datetime import datetime


class ViewAll(MethodView):

    def __init__(self):
        # 不判断是否非法，默认为第一页数据
        self.page_num = request.args.get('page_num', 1, type=int)
        # 每页展示的数据，可被前台用户自行调整，如未设置默认为10条一页
        # 此处分页设置为1为方便调试，正式环境上应该设置为10
        self.page_size = request.args.get('page_size', 1, type=int)
        self.sort_by = request.args.get('sort_by', 'created_at')
        self.sort_dir = request.args.get('sort_dir', 'desc')

    @http_auth.login_required
    def get(self):
        try:
            if self.sort_dir not in "desc|asc" or self.sort_by not in "name|created_at|updated_at|user_name":
                return jsonify({
                    "status": {
                        "code": 40030,
                        "is_error": True,
                        "message": "Sorting & Pagination Query Parameters Illegal"
                    }
                })
            if self.sort_dir == 'desc':
                result = TextAnalyzer.query.filter_by(is_valid=True).order_by(self.sort_by.desc()
                                                 ).paginate(self.page_num, self.page_size, error_out=False)
            if self.sort_dir == 'asc':
                result = TextAnalyzer.query.filter_by(is_valid=True).order_by("-"+self.sort_by.desc()
                                                     ).paginate(self.page_num, self.page_size, error_out=False)
            page_total = result.pages
            result_set = []
            for items in result.items:
                result_set.append(dict({"id": items.id, "name": items.name, "description": items.description,
                                        "user_name": items.user_name, "user_id": items.user_id,
                                        "created_at": items.created_at, "updated_at": items.updated_at}))
            return jsonify({
                            "text_analyzers": result_set,
                            "status": {
                                "code": 200,
                                "is_error": False,
                                "message": "Successfully Retrieve All Users' Information"
                            },
                            "pages": {
                                "page": self.page_num,
                                "per_page": self.page_size,
                                "page_total": page_total,
                                "sort_by": self.sort_by,
                                "sort_dir": self.sort_dir
                            }
                })
        except Exception as e:
            raise e

        """
        分页展示数据，self.page为前端传过来的当前页面数，
        per_page=1为每个页面展示的数据为一行（此处为方便测试展示一行，之后正式环境应改成每页展示10行数据）
        如果error_out为False则下列情况下不抛出404异常
        """
        # try:
        #     result = TextAnalyzer.query.all()
        #     result_set = []
        #     for result_model in result:
        #         print(result_model.name)
        #         result_set.append(dict({"id": result_model.id, "name": result_model.name,
        #                                 "creator": result_model.name, "created_at": result_model.created_at}))
        #     return jsonify({
        #                     "text_analyzers": result_set,
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
    def get(self):
        try:
            result = TextAnalyzer.query.filter_by(id=self.id, is_valid=True).first()
            if result:
                sentences_list = result.sentences.split("#")
                keywords_list = result.keywords.split("#")
                return jsonify({
                            "text_analyzer": {
                                "id": result.id,
                                "name": result.name,
                                "description": result.description,
                                "user_id": result.user_id,
                                "user_name": result.user_name,
                                "target": result.target,
                                "created_at": result.created_at,
                                "updated_at": result.updated_at,
                                "prob": result.prob,
                                "sentences": sentences_list
                            },
                            "keywords": keywords_list,
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
                        "message": "Cannot Find Text Analyzer With Given ID"


                    }
                })
        except Exception as e:
            raise e


class CreateText(MethodView):

    def __init__(self):
        self.name = request.json.get("name")
        self.sentences = request.json.get("sentences")
        self.keywords = request.json.get("keywords")
        self.prob = request.json.get("prob")
        self.target = request.json.get("target")
        self.description = request.json.get("description")

    @http_auth.login_required
    def post(self):
        try:
            if self.name is None or self.sentences is None or self.prob is None or self.keywords is None \
                    or self.target is None:
                return jsonify({
                        'status': {
                            "code": 40017,
                            "is_error": True,
                            "message": "Cannot Created Text Because of the missing information"
                        }
                })
            result = TextAnalyzer.query.filter_by(name=self.name, is_valid=True).first()
            if result:
                return jsonify({
                    'status': {
                        "code": 40011,
                        "is_error": True,
                        "message": "Cannot Create Text Analyzer Because of Conflicted Name"
                    }
                })
            # 存入数据库中以#号分割
            str_sentences = '#'.join(self.sentences)
            str_keywords = '#'.join(self.keywords)
            text = TextAnalyzer(name=self.name, sentences=str_sentences, prob=self.prob, keywords=str_keywords,
                                target=self.target)
            db.session.add(text)
            db.session.commit()
            return jsonify({
                "text_analyzer": {
                    "id": text.id,
                    "name": text.name,
                    "creator": g.user.user_id,
                    "created_at": datetime.now,
                    "prob": text.prob,
                    "target": 1,
                    "sentences": self.sentences,
                    "keywords": self.keywords
                },
                "status": {
                    "code": 200,
                    "is_error": False,
                    "message": "Successfully Create Text Analyzer"
                }
            })
        except Exception as e:
            raise e


class UpdateText(MethodView):

    def __init__(self):
        self.id = request.args.get('id')
        self.name = request.json.get("name")
        self.sentences = request.json.get("sentences")
        self.keywords = request.json.get("keywords")
        self.target = request.json.get("target")
        self.description = request.json.get("description")
        self.prob = request.json.get("prob")

    @http_auth.login_required
    def put(self):
        try:
            if self.name is None and self.sentences is None and self.keywords is None \
                    and self.target is None and self.description is None and \
                    self.prob is None:
                return jsonify({
                    "status": {
                        "code": 40017,
                        "is_error": True,
                        "message": "Cannot Update Text Because of the missing information"

                    }
                })
            result = TextAnalyzer.query.filter_by(id=self.id, is_valid=True).first()
            if result is None:
                return jsonify({
                    "status": {
                        "code": 40010,
                        "is_error": True,
                        "message": "Cannot Find Text Analyzer With Given ID"

                    }
                })
            if self.name != result.name:
                exist_text = TextAnalyzer.query.filter_by(id=self.id, is_valid=True).first()
                if exist_text:
                    return jsonify({
                        "status": {
                            "code": 40016,
                            "is_error": True,
                            "message": "Cannot Update Text Because of the Conflicted Name"

                        }
                    })
            if self.name is not None and self.name != result.name:
                result.name = self.name
            if self.sentences is not None:
                str_sentences = '#'.join(self.sentences)
                result.sentences = str_sentences
            if self.keywords is not None and self.keywords != result.keywords:
                str_keywords = '#'.join(self.keywords)
                result.keywords = str_keywords
            if self.target is not None and self.target != result.target:
                result.target = self.target
            if self.description is not None and self.description != result.description:
                result.description = self.description
            if self.prob is not None and self.prob != result.prob:
                result.prob = self.prob
            result.updated_at = datetime.now
            db.session.add(result)
            db.session.commit()
            return jsonify({
                "text_analyzer": {
                    "id": self.id,
                    "name": self.name,
                    "creator": result.user_id,
                    "created_at": result.created_at,
                    "prob": result.prob,
                    "target": result.target,
                    "sentences": self.sentences,
                    "keywords": self.keywords
                },
                "status": {
                    "code": 200,
                    "is_error": False,
                    "message": "Successfully Update Text Analyzer"
                }
            })
        except Exception as e:
            raise e


class DeleteText(MethodView):

    def __init__(self):
        self.id = request.args.get('id')

    @http_auth.login_required
    def delete(self):
        try:
            result = TextAnalyzer.query.filter_by(id=self.id, is_valid=True).first()
            if result is None:
                return jsonify({
                    "status": {
                        "code": 40010,
                        "is_error": True,
                        "message": "Cannot Find Text Analyzer With Given ID"

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
                    "message": "Successfully Delete Text Analyzer"
                }
            })
        except Exception as e:
            raise e

