# -*- coding: utf-8 -*-

from flask_script import Manager
from app import app,db

manager = Manager(app)


@manager.command
def init():
    from models.api import Api
    from models.app import App
    from models.menu import ParentMenu,Menu,MenuHasApi
    from models.role import Role,RoleHasApi,RoleHasMenu
    from models.user import User,UserHasRole
    # 应用
    from models.node import Node,NodeClas,NodesHasTag,NodesHasTask
    from models.service import Service,ServicesHasTag
    from models.tag import Tag
    from models.task import Task
    db.create_all(app=app)


if __name__ == "__main__":
    manager.run()
