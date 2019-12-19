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
