# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_restful import Api
from applications.app_manage import Login,Logout,Register,SendCode
from applications.menu_manage import MenuAction,ParentMenuAction,MenuHasApiAction

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
mail = Mail(app)
api = Api(app)


api.add_resource(Login,'/login')
api.add_resource(Logout,'/logout')
api.add_resource(Register,'/register')
api.add_resource(SendCode,'/send/email')
api.add_resource(MenuAction,'/menu')
api.add_resource(ParentMenuAction,'/parent/menu')
api.add_resource(MenuHasApiAction,'/menu/auth')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'],
            threaded=True)
