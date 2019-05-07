import os
from datetime import datetime

from flask import jsonify, request
from flask.views import MethodView

from .. import db, http_auth
from api.pattern_analyzers.models import PatternAnalyzerModel
from api.pattern_analyzers.models import PatternNodesModel

global PATTERN_ANALYZER_PAGE_SIZE
try:
    PATTERN_ANALYZER_PAGE_SIZE = os.environ['PATTERN_ANALYZER_PAGE_SIZE']
except KeyError as e:
    PATTERN_ANALYZER_PAGE_SIZE = 2
    #TODO: Handle Environment Variable Missing Problem
    print("KeyError")
    pass

class ViewAll(MethodView):

    def __init__(self):
        try:
            self.page_num = request.args.get('page_num', 1, type=int)
            self.page_size= request.args.get('page_size', PATTERN_ANALYZER_PAGE_SIZE, type=int)
            self.sort_by= request.args.get('sort_by', PATTERN_ANALYZER_PAGE_SIZE, type=string)
            self.sort_mode= request.args.get('page_ssort_modeize', PATTERN_ANALYZER_PAGE_SIZE, type=string)
        except TypeError as e:
            #TODO: Handle Query Parameter Type Error Problem
            print("TypeError")
            pass
        except:
            #TODO: Handle General ERROR
            print("General Error")
            pass

    # @http_auth.login_required
    def get(self):
        try:
            pattern_analyzers = PatternAnalyzerModel.query.with_entities(
                PatternAnalyzerModel.id, 
                PatternAnalyzerModel.name, 
                PatternAnalyzerModel.description,
                PatternAnalyzerModel.created_at
            ).filter_by(is_valid=True)
            .order_by()
            .paginate(
                self.page_num, 
                self.page_size, 
                error_out=False
            )
            result_set = []
            for pattern_analyzer in pattern_analyzers.items:
                result_set.append(dict({
                    "id": pattern_analyzer.id, 
                    "name": pattern_analyzer.name,
                    "description": pattern_analyzer.description,
                    "created_at": pattern_analyzer.created_at
                }))
            return jsonify({
                "pattern_analyzers": result_set,
                "pages": {
                    "page_num": 2,        # 当前页
                    "page_size": 1,       # 每页显示多少行数据，此处为方便测试改成每页1行
                    "page_total": 2,      # 总页数
                    "sort_by": "user_name",	   # 当前分页的采用的Key
                    "sort_dir": "asc",    # 当前分页的排序方式
                },
                "status": {
                    "code": 200,
                    "is_error": False,
                    "message": "Successfully Retrieve All Analyzers' Information"
                }
            })
        except Exception as e:
            raise e


class ViewOne(MethodView):

    def __init__(self):
        pass

    @http_auth.login_required
    def get(self):
        pass


class CreatePattern(MethodView):

    def __init__(self):
        pass

    @http_auth.login_required
    def post(self):
        pass


class UpdateNodeNew(MethodView):

    def __init__(self):
        pass

    @http_auth.login_required
    def put(self):
        pass


class UpdateNodeUpdate(MethodView):

    def __init__(self):
        pass

    @http_auth.login_required
    def put(self):
        pass


class UpdateNodeDelete(MethodView):

    def __init__(self):
        pass

    @http_auth.login_required
    def put(self):
        pass


class DeletePattern(MethodView):

    def __init__(self):
        pass

    @http_auth.login_required
    def delete(self):
        pass
