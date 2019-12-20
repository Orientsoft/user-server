# -*- coding: utf-8 -*-
from flask import request, session
from flask_restful import Resource


class RoleAction(Resource):
    def __init__(self):
        self.app_id = session.get('app_id')

    def post(self):
        from models.role import Role
        from app import db
        a = Role()
        a.app_id = self.app_id
        a.name = request.json.get('name')
        db.session.add(a)
        db.session.commit()

    def get(self):
        from models.role import Role
        dataObj = Role.query.filter_by(app_id=self.app_id).all()
        result = []
        for d in dataObj:
            result.append({
                "id":d.id,
                "name":d.name
            })
        return result

    def patch(self):
        from models.role import Role
        from app import db
        id = request.json.get('id')
        m = Role.query.filter_by(app_id=self.app_id, id=id).first()
        if m:
            name = request.json.get('name', None)
            if name:
                m.name = name
            db.session.commit()
        else:
            return '权限错误', 400

    def delete(self):
        from models.role import Role
        from app import db
        id = request.json.get('id')
        m = Role.query.filter_by(app_id=self.app_id, id=id).first()
        if m:
            db.session.delete(m)
            db.session.commit()
