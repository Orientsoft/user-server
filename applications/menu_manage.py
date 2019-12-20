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
        from models.utils import model_to_dict
        dataObj = Menu.query.filter_by(app_id=self.app_id).all()
        result = model_to_dict(dataObj)
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
        from models.menu import Menu
        from app import db
        id = request.json.get('id')
        m = Menu.query.filter_by(app_id=self.app_id, id=id).first()
        if m:
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
        id = request.json.get('id')
        m = ParentMenu.query.filter_by(app_id=self.app_id, id=id).first()
        if m:
            db.session.delete(m)
            db.session.commit()


class MenuHasApiAction(Resource):
    def __init__(self):
        self.app_id = session.get('app_id')

    # 批量添加菜单拥有的接口
    def post(self):
        from models.menu import MenuHasApi
        from app import db
        try:
            menu_id = request.json.get('menu_id')
            if not self.check_menu(menu_id):
                return '权限错误', 400
            now_apis = request.json.get('api_ids')
            result = MenuHasApi.query.with_entities(MenuHasApi.api_id).filter_by(menu_id=menu_id).all()
            old_apis = []
            for r in result:
                print(r)
                old_apis.append(str(r[0]))
            need_delete = list(set(old_apis) - set(now_apis))
            need_add = list(set(now_apis) - set(old_apis))
            for n in need_add:
                if self.check_api(n):
                    m = MenuHasApi()
                    m.menu_id = menu_id
                    m.api_id = n
                    db.session.add(m)
            for d in need_delete:
                if self.check_api(d):
                    m = MenuHasApi.query.filter_by(menu_id=menu_id, api_id=d).first()
                    db.session.delete(m)
            db.session.commit()
        except Exception as e:
            db.session.rollback()

    def get(self):
        # 根据menu_id查询对应的api_id
        from models.menu import MenuHasApi
        from models.utils import model_to_dict
        menu_id = request.args.get('menu_id')
        if not self.check_menu(menu_id):
            return '权限错误', 400
        dataObj = MenuHasApi.query.filter_by(menu_id=menu_id).all()
        result = []
        for d in dataObj:
            result.append({
                'menu_id':d.menu_id,
                'api_id':d.api_id,
                'menu_name':d.menu.name,
                'menu_refer_path':d.menu.refer_path,
                'menu_partent_id':d.menu.parent_id,
                'api_path':d.api.path,
                'api_method':d.api.method,
                'api_remark':d.api.remark,
            })
        return result

    def check_menu(self, menu_id):
        from models.menu import Menu
        m = Menu.query.get(menu_id)
        if m is None:
            return False
        if m.app_id == self.app_id:
            return True
        else:
            return False

    def check_api(self, api_id):
        from models.api import Api
        a = Api.query.get(api_id)
        if a is None:
            return False
        if a.app_id == self.app_id:
            return True
        else:
            return False
