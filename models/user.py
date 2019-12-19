# coding: utf-8
from app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(45))
    remark = db.Column(db.String(200))
    createdAt = db.Column(db.DateTime)
    lastLogin = db.Column(db.DateTime)
    app_id = db.Column(db.ForeignKey('app.id'), nullable=False, index=True)

    app = db.relationship('App')



class UserHasRole(db.Model):
    __tablename__ = 'user_has_role'

    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    role_id = db.Column(db.ForeignKey('role.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id = db.Column(db.INTEGER, primary_key=True)

    role = db.relationship('Role')
    user = db.relationship('User')




