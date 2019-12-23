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
                "id": d.id,
                "name": d.name
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


class RoleHasApiAction(Resource):
    def __init__(self):
        self.app_id = session.get('app_id')

    # 批量添加角色拥有的接口
    def post(self):
        from models.role import Role, RoleHasApi
        from models.api import Api

        from app import db
        try:
            role_id = request.json.get('role_id')
            if not Role.check_role(self.app_id, role_id):
                return '权限错误', 400
            now_apis = request.json.get('api_ids')
            old_apis = RoleHasApi.get_api(role_id)
            need_delete = list(set(old_apis) - set(now_apis))
            need_add = list(set(now_apis) - set(old_apis))
            for n in need_add:
                if Api.check_api(self.app_id, n):
                    m = RoleHasApi()
                    m.role_id = role_id
                    m.api_id = n
                    db.session.add(m)
            for d in need_delete:
                if Api.check_api(self.app_id, d):
                    m = RoleHasApi.query.filter_by(role_id=role_id, api_id=d).first()
                    db.session.delete(m)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    def get(self):
        # 根据role_id查询对应的api_id。
        # 需返回已分配的，和未分配的API
        from models.role import Role, RoleHasApi
        from models.api import Api
        returnObj = {}
        assigned_apis = []
        not_assigned_apis = []
        role_id = request.args.get('role_id')
        if not Role.check_role(self.app_id, role_id):
            return '权限错误', 400

        assigned_apis_in_db = RoleHasApi.query.filter_by(
            role_id=role_id).all()
        all_apis_in_db = Api.query.filter_by(app_id=self.app_id).all()

        assigned_api_ids = []
        for a in assigned_apis_in_db:
            assigned_api_ids.append(a.api_id)
            assigned_apis.append(
                {'id': a.api_id, 'path': a.api.path, 'method': a.api.method, 'remark': a.api.remark})
        assigned_api_ids = set(assigned_api_ids)

        for a in all_apis_in_db:
            if a.id not in assigned_api_ids:
                not_assigned_apis.append(
                    {'id': a.id, 'path': a.path, 'method': a.method, 'remark': a.remark})

        returnObj['not_assigned_apis'] = not_assigned_apis
        returnObj['assigned_apis'] = assigned_apis

        return returnObj


class RoleHasMenuAction(Resource):
    def __init__(self):
        self.app_id = session.get('app_id')

    # 批量添加角色拥有的菜单，添加时自动操作role_has_api
    def post(self):
        from models.role import Role, RoleHasApi, RoleHasMenu
        from models.menu import Menu, MenuHasApi

        from app import db
        try:
            role_id = request.json.get('role_id')
            if not Role.check_role(self.app_id, role_id):
                return '权限错误', 400
            now_menus = request.json.get('menu_ids')
            old_menus = RoleHasMenu.get_menu(role_id)
            need_delete = list(set(old_menus) - set(now_menus))
            need_add = list(set(now_menus) - set(old_menus))
            for n in need_add:
                if Menu.check_menu(self.app_id, n):
                    m = RoleHasMenu()
                    m.role_id = role_id
                    m.menu_id = n
                    db.session.add(m)
                    # 查询menu_has_api,   menu_id拥有的俄api_id,自动添加到role_has_api中
                    temp = MenuHasApi.get_api(n)
                    for x in temp:
                        rha = RoleHasApi()
                        rha.role_id = role_id
                        rha.api_id = x
                        db.session.add(rha)

            for d in need_delete:
                if Menu.check_menu(self.app_id, d):
                    m = RoleHasMenu.query.filter_by(role_id=role_id, menu_id=d).first()
                    # 查询 menu_has_api,  menu_id拥有的api_id，删除role_has_api
                    temp = MenuHasApi.get_api(m.menu_id)
                    for x in temp:
                        c = RoleHasApi.query.filter_by(role_id=role_id, api_id=x).first()
                        db.session.delete(c)
                    db.session.delete(m)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    def get(self):
        # 根据role_id查询对应的menu_id。
        # 需返回已分配的，和未分配的菜单
        from models.role import Role, RoleHasApi,RoleHasMenu
        from models.menu import Menu
        returnObj = {}
        assigned_menus = []
        not_assigned_menus = []
        role_id = request.args.get('role_id')
        if not Role.check_role(self.app_id, role_id):
            return '权限错误', 400

        assigned_menus_in_db = RoleHasMenu.query.filter_by(
            role_id=role_id).all()
        all_menus_in_db = Menu.query.filter_by(app_id=self.app_id).all()

        assigned_menu_ids = []
        for a in assigned_menus_in_db:
            assigned_menu_ids.append(a.menu_id)
            assigned_menus.append(
                {'id': a.menu_id, 'name': a.menu.name, 'refer_path': a.menu.refer_path, 'remark': a.menu.parent_id})
        assigned_menu_ids = set(assigned_menu_ids)

        for a in all_menus_in_db:
            if a.id not in assigned_menu_ids:
                not_assigned_menus.append(
                    {'id': a.id, 'name': a.name, 'refer_path': a.refer_path, 'parent_id': a.parent_id,'parent_name':a.parent.name})

        returnObj['not_assigned_menus'] = not_assigned_menus
        returnObj['assigned_menus'] = assigned_menus

        return returnObj
