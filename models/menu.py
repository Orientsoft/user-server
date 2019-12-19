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


class MenuHasApi(db.Model):
    __tablename__ = 'menu_has_api'

    menu_id = db.Column(db.ForeignKey('menu.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    api_id = db.Column(db.ForeignKey('api.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id = db.Column(db.INTEGER, primary_key=True)

    api = db.relationship('Api')
    menu = db.relationship('Menu')
