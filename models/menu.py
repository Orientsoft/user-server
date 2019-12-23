# coding: utf-8
from app import db


class ParentMenu(db.Model):
    __tablename__ = 'parent_menu'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45))
    app_id = db.Column(db.ForeignKey('app.id'), nullable=False, index=True)

    app = db.relationship('App')


class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    refer_path = db.Column(db.String(200))
    parent_id = db.Column(db.ForeignKey('parent_menu.id'), index=True)
    app_id = db.Column(db.ForeignKey('app.id'), nullable=False, index=True)

    app = db.relationship('App')
    parent = db.relationship('ParentMenu')

    @staticmethod
    def check_menu(app_id, menu_id):
        m = Menu.query.get(menu_id)
        if m is None:
            return False
        if m.app_id == app_id:
            return True
        else:
            return False


class MenuHasApi(db.Model):
    __tablename__ = 'menu_has_api'
    __table_args__ = (
        db.Index('ue_menuid_apiid', 'menu_id', 'api_id', unique=True),
    )

    menu_id = db.Column(db.ForeignKey('menu.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    api_id = db.Column(db.ForeignKey('api.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id = db.Column(db.INTEGER, primary_key=True)

    api = db.relationship('Api')
    menu = db.relationship('Menu')

    @staticmethod
    def get_api(menu_id):
        apis = []
        try:
            result = MenuHasApi.query.with_entities(MenuHasApi.api_id).filter_by(menu_id=menu_id).all()
            for r in result:
                apis.append(str(r[0]))
        except Exception as e:
            pass
        finally:
            return apis
