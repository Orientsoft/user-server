# -*- coding: utf-8 -*-
from flask import request, session
from flask_restful import Resource
import datetime
import hashlib
import uuid


class UserAction(Resource):
    def __init__(self):
        self.app_id = session.get('app_id')

    def post(self):
        from models.user import User
        from app import db
        a = User()
        a.app_id = self.app_id
        a.id = uuid.uuid1().hex
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
                "id": d.id,
                "name": d.name,
                "remark": d.remark,
                "createdAt": d.createdAt.strftime('%Y-%m-%d %H:%M:%S') if isinstance(d.createdAt,datetime.datetime) else d.createdAt,
                "lastLogin": d.lastLogin.strftime('%Y-%m-%d %H:%M:%S') if isinstance(d.lastLogin,datetime.datetime) else d.lastLogin
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


class UserHasRoleAction(Resource):
    def __init__(self):
        self.app_id = session.get('app_id')

    # 批量添加用户拥有的角色
    def post(self):
        from models.user import UserHasRole, User
        from models.role import Role
        from app import db
        try:
            user_id = request.json.get('id')
            if not User.check_user(self.app_id, user_id):
                return '权限错误', 400
            now_roles = request.json.get('role_ids')
            old_roles = UserHasRole.get_role(user_id)
            need_delete = list(set(old_roles) - set(now_roles))
            need_add = list(set(now_roles) - set(old_roles))
            for n in need_add:
                if Role.check_role(self.app_id, n):
                    m = UserHasRole()
                    m.user_id = user_id
                    m.role_id = n
                    db.session.add(m)
            for d in need_delete:
                if Role.check_role(self.app_id, d):
                    m = UserHasRole.query.filter_by(user_id=user_id, role_id=d).first()
                    db.session.delete(m)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    def get(self):
        # 根据user_id 查询role_id。
        # 需返回已分配的role，和未分配的role
        from models.user import UserHasRole, User
        from models.role import Role
        returnObj = {}
        assigned_roles = []
        not_assigned_roles = []
        user_id = request.args.get('id')
        if not User.check_user(self.app_id, user_id):
            return '权限错误', 400
        assigned_roles_in_db = UserHasRole.query.filter_by(
            user_id=user_id).all()
        all_roles_in_db = Role.query.filter_by(app_id=self.app_id).all()

        assigned_role_ids = []
        for role in assigned_roles_in_db:
            assigned_role_ids.append(role.role_id)
            assigned_roles.append(
                {'id': role.role_id, 'role': role.role.name})
        assigned_role_ids = set(assigned_role_ids)

        for role in all_roles_in_db:
            if role.id not in assigned_role_ids:
                not_assigned_roles.append(
                    {'id': role.id, 'role': role.name})
        returnObj['not_assigned_roles'] = not_assigned_roles
        returnObj['assigned_roles'] = assigned_roles
        return returnObj
