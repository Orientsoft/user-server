# coding: utf-8
from app import db


class App(db.Model):
    __tablename__ = 'app'

    id = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(45), nullable=False,unique=True)
    password = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    public_key = db.Column(db.String(2000))
    private_key = db.Column(db.String(2000))
    check = db.Column(db.Boolean, nullable=False, server_default='0')

    @staticmethod
    def check_email_exist(email):
        a = App.query.filter_by(email=email).first()
        if a:
            return True
        else:
            return False
