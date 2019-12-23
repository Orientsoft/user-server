# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_restful import Api
from applications.app_manage import Login,Logout,Register,SendCode
from applications.menu_manage import MenuAction,ParentMenuAction,MenuHasApiAction
from applications.api_manage import ApiAction
from applications.user_manage import UserAction,UserHasRoleAction
from applications.role_manage import RoleAction,RoleHasApiAction,RoleHasMenuAction

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
api.add_resource(ApiAction,'/api')
api.add_resource(UserAction,'/user')
api.add_resource(UserHasRoleAction,'/user/auth')
api.add_resource(RoleAction,'/role')
api.add_resource(RoleHasApiAction,'/role/api/auth')
api.add_resource(RoleHasMenuAction,'/role/menu/auth')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'], host=app.config['HOST'], port=app.config['PORT'],
            threaded=True)
