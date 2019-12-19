# coding: utf-8
from app import db


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45))
    app_id = db.Column(db.ForeignKey('app.id'), nullable=False, index=True)

    app = db.relationship('App')


class RoleHasApi(db.Model):
    __tablename__ = 'role_has_api'

    role_id = db.Column(db.ForeignKey('role.id'), nullable=False, index=True)
    api_id = db.Column(db.ForeignKey('api.id'), nullable=False, index=True)
    id = db.Column(db.INTEGER, primary_key=True)

    api = db.relationship('Api')
    role = db.relationship('Role')

class RoleHasMenu(db.Model):
    __tablename__ = 'role_has_menu'

    role_id = db.Column(db.ForeignKey('role.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    menu_id = db.Column(db.ForeignKey('menu.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id = db.Column(db.INTEGER, primary_key=True)

    menu = db.relationship('Menu')
    role = db.relationship('Role')
