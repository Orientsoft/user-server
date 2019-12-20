# coding: utf-8
from app import db


class Api(db.Model):
    __tablename__ = 'api'

    id = db.Column(db.INTEGER, primary_key=True)
    path = db.Column(db.String(45))
    method = db.Column(db.String(45))
    remark = db.Column(db.String(45))
    app_id = db.Column(db.ForeignKey('app.id'), nullable=False, index=True)

    app = db.relationship('App')

    @staticmethod
    def check_api(app_id, api_id):
        a = Api.query.get(api_id)
        if a is None:
            return False
        if a.app_id == app_id:
            return True
        else:
            return False
