# -*- coding: utf-8 -*-
from flask import request, session
from flask_restful import Resource


class MenuAction(Resource):
    def __init__(self):
        self.app_id = session.get('app_id')

    def post(self):
        from models.menu import Menu
        from app import db
        m = Menu()
        m.app_id = self.app_id
        m.name = request.json.get('name')
        m.parent_id = request.json.get('parent_id', None)
        m.refer_path = request.json.get('refer_path', None)
        db.session.add(m)
        db.session.commit()

    def get(self):
        from models.menu import Menu
        result = []
        dataObj = Menu.query.filter_by(app_id=self.app_id).all()
        for d in dataObj:
            result.append({
                'id': d.id,
                'name': d.name,
                'refer_path': d.refer_path,
                'parent_id': d.parent_id,
                'parent_name': d.parent.name if d.parent else ''
            })
        return result

    def patch(self):
        from models.menu import Menu
        from app import db
        id = request.json.get('id')
        m = Menu.query.filter_by(app_id=self.app_id, id=id).first()
        if m:
            name = request.json.get('name', None)
            parent_id = request.json.get('parent_id', None)
            refer_path = request.json.get('refer_path', None)
            if name:
                m.name = name
            if parent_id:
                m.parent_id = parent_id
            if refer_path:
                m.refer_path = refer_path
            db.session.commit()
        else:
            return '权限错误', 400

    def delete(self):
        from models.menu import Menu, MenuHasApi
        from models.role import RoleHasMenu, RoleHasApi
        from app import db
        id = request.json.get('id')
        m = Menu.query.filter_by(app_id=self.app_id, id=id).first()
        if m:
            # 查角色，和api
            roles = RoleHasMenu.get_role(m.id)
            apis = MenuHasApi.get_api(m.id)
            result = RoleHasApi.query.filter(RoleHasApi.api_id.in_(apis)).filter(RoleHasApi.role_id.in_(roles)).all()
            for r in result:
                db.session.delete(r)
            db.session.delete(m)
            db.session.commit()


class ParentMenuAction(Resource):
    def __init__(self):
        self.app_id = session.get('app_id')

    def post(self):
        from models.menu import ParentMenu
        from app import db
        m = ParentMenu()
        m.app_id = self.app_id
        m.name = request.json.get('name')
        db.session.add(m)
        db.session.commit()

    def get(self):
        from models.menu import ParentMenu
        from models.utils import model_to_dict
        dataObj = ParentMenu.query.filter_by(app_id=self.app_id).all()
        result = model_to_dict(dataObj)
        return result

    def patch(self):
        from models.menu import ParentMenu
        from app import db
        id = request.json.get('id')
        m = ParentMenu.query.filter_by(app_id=self.app_id, id=id).first()
        if m:
            name = request.json.get('name', None)
            if name:
                m.name = request.json.get('name')
                db.session.commit()
        else:
            return '权限错误', 400

    def delete(self):
        from models.menu import ParentMenu
        from app import db
        try:
            id = request.json.get('id')
            m = ParentMenu.query.filter_by(app_id=self.app_id, id=id).first()
            if m:
                db.session.delete(m)
                db.session.commit()
        except:
            db.session.rollback()


class MenuHasApiAction(Resource):
    def __init__(self):
        self.app_id = session.get('app_id')

    # 批量添加菜单拥有的接口
    def post(self):
        from models.menu import MenuHasApi, Menu
        from models.api import Api
        from models.role import RoleHasApi, RoleHasMenu

        from app import db
        try:
            menu_id = request.json.get('id')
            if not Menu.check_menu(self.app_id, menu_id):
                return '权限错误', 400
            now_apis = request.json.get('api_ids')
            old_apis = MenuHasApi.get_api(menu_id)
            need_delete = list(set(old_apis) - set(now_apis))
            need_add = list(set(now_apis) - set(old_apis))
            # 根据menu_id 查询roles
            roles = RoleHasMenu.get_role(menu_id)
            for n in need_add:
                if Api.check_api(self.app_id, n):
                    m = MenuHasApi()
                    m.menu_id = menu_id
                    m.api_id = n
                    db.session.add(m)
                    # 将role_id,n写入role_has_api
                    for r in roles:
                        rha = RoleHasApi()
                        rha.role_id = r
                        rha.api_id = n
                        db.session.add(rha)
            for d in need_delete:
                if Api.check_api(self.app_id, d):
                    m = MenuHasApi.query.filter_by(menu_id=menu_id, api_id=d).first()
                    # 删除role_has_api中角色对应的api
                    temp = RoleHasApi.query.filter(RoleHasApi.api_id == d, RoleHasApi.role_id.in_(roles)).all()
                    for t in temp:
                        db.session.delete(t)
                    db.session.delete(m)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    def get(self):
        # 根据menu_id查询对应的api_id。
        # 需返回已分配的，和未分配的API
        from models.menu import MenuHasApi, Menu
        from models.api import Api
        returnObj = {}
        assigned_apis = []
        not_assigned_apis = []
        menu_id = request.args.get('id')
        if not Menu.check_menu(self.app_id, menu_id):
            return '权限错误', 400

        assigned_apis_in_db = MenuHasApi.query.filter_by(
            menu_id=menu_id).all()
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
