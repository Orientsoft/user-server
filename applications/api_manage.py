# -*- coding: utf-8 -*-
from flask import request, session
from flask_restful import Resource


class ApiAction(Resource):
    def __init__(self):
        self.app_id = session.get('app_id')

    def post(self):
        from models.api import Api
        from app import db
        a = Api()
        a.app_id = self.app_id
        a.path = request.json.get('path')
        a.method = request.json.get('method', None)
        a.remark = request.json.get('remark', None)
        db.session.add(a)
        db.session.commit()

    def get(self):
        from models.api import Api
        from models.utils import model_to_dict
        dataObj = Api.query.filter_by(app_id=self.app_id).all()
        result = model_to_dict(dataObj)
        return result

    def patch(self):
        from models.api import Api
        from app import db
        id = request.json.get('id')
        m = Api.query.filter_by(app_id=self.app_id, id=id).first()
        if m:
            path = request.json.get('path', None)
            method = request.json.get('method', None)
            remark = request.json.get('remark', None)
            if path:
                m.path = path
            if method:
                m.method = method
            if remark:
                m.remark = remark
            db.session.commit()
        else:
            return '权限错误', 400

    def delete(self):
        from models.api import Api
        from app import db
        id = request.json.get('id')
        m = Api.query.filter_by(app_id=self.app_id, id=id).first()
        if m:
            db.session.delete(m)
            db.session.commit()
