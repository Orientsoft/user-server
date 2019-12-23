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

    @staticmethod
    def check_user(app_id, user_id):
        a = User.query.get(user_id)
        if a is None:
            return False
        if a.app_id == app_id:
            return True
        else:
            return False


class UserHasRole(db.Model):
    __tablename__ = 'user_has_role'

    user_id = db.Column(db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    role_id = db.Column(db.ForeignKey('role.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    id = db.Column(db.INTEGER, primary_key=True)

    role = db.relationship('Role')
    user = db.relationship('User')

    @staticmethod
    def get_role(user_id):
        roles = []
        try:
            result = UserHasRole.query.with_entities(UserHasRole.role_id).filter_by(user_id=user_id).all()
            for r in result:
                roles.append(str(r[0]))
        except:
            pass
        finally:
            return roles
