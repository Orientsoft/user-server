# -*- coding: utf-8 -*-
from flask import request, session
import uuid
import hashlib
from flask_mail import Message
import random
from ext import redisHelper
import re
from common.tools import code_send_limit
from flask_restful import Resource

redis = redisHelper()


class Login(Resource):
    def post(self):
        from models.app import App
        email = request.json.get('email').strip()
        password = request.json.get('password')
        a = App.query.filter_by(email=email, password=password).first()
        if a:
            session['app_id'] = a.id
            return '登陆成功', 200
        else:
            return '账号或密码错误', 400


class Register(Resource):
    def post(self):
        from app import db
        from models.app import App

        try:
            email = request.json.get('email').strip()
            # 校验邮件验证码
            code = redis.get(email)
            if not code:
                return '验证码已失效', 400
            if code != request.json.get('code'):
                return '验证码错误', 400
            r = App()
            r.email = email
            r.name = request.json.get('name')
            r.id = uuid.uuid1().hex
            r.password = hashlib.sha256(request.json.get('password').strip().encode('utf8')).hexdigest()
            db.session.add(r)
            db.session.commit()
            return '注册成功', 200
        except:
            db.session.rollback()
            return '注册失败', 400


class SendCode(Resource):
    def post(self):
        email = request.json.get('email').strip()
        if not re.match(r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$', email):
            return '邮箱格式错误'
        if code_send_limit(email):
            return '发送频繁，请稍后再试'
        from models.app import App
        from app import mail
        # 校验邮箱是否可用
        if App.check_email_exist(email):
            return '邮箱已被使用', 400
        code = random.randrange(100000, 999999)
        msg = Message("验证码-User", body="您好，您正在进行身份验证，本次操作的验证码为：{}，请在10分钟内完成验证。".format(code), recipients=[email])
        mail.send(msg)
        redis.set(email, code, ex=10 * 60)
        return '发送成功', 200


class Logout(Resource):
    def get(self):
        session.clear()
        return '退出成功', 200
