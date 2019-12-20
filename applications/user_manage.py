# -*- coding: utf-8 -*-
from flask import request, session
from flask_restful import Resource
import datetime
import hashlib


class UserAction(Resource):
    def __init__(self):
        self.app_id = session.get('app_id')

    def post(self):
        from models.user import User
        from app import db
        a = User()
        a.app_id = self.app_id
        a.name = request.json.get('name')
        a.password = hashlib.sha256(request.json.get('password').strip().encode('utf8')).hexdigest()
        a.remark = request.json.get('remark', None)
        a.createdAt = datetime.datetime.now()
        db.session.add(a)
        db.session.commit()

    def get(self):
        from models.user import User
        dataObj = User.query.filter_by(app_id=self.app_id).all()
        result = []
        for d in dataObj:
            result.append({
                "id":d.id,
                "name":d.name,
                "remark":d.remark,
                "createAt":d.createAt,
                "lastLogin":d.lastLogin
            })
        return result

    def patch(self):
        from models.user import User
        from app import db
        id = request.json.get('id')
        m = User.query.filter_by(app_id=self.app_id, id=id).first()
        if m:
            name = request.json.get('name', None)
            password = request.json.get('password', None)
            remark = request.json.get('remark', None)
            if name:
                m.name = name
            if password:
                m.password = hashlib.sha256(password.strip().encode('utf8')).hexdigest()
            if remark:
                m.remark = remark
            db.session.commit()
        else:
            return '权限错误', 400

    def delete(self):
        from models.user import User
        from app import db
        id = request.json.get('id')
        m = User.query.filter_by(app_id=self.app_id, id=id).first()
        if m:
            db.session.delete(m)
            db.session.commit()
