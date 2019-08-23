#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-08-29 18:12

from flask import Flask, Blueprint
from flask_restful import Api
from flask_uploads import patch_request_class, configure_uploads


from upload.views import bp,photos


from config import config

def create_app(envv):
    app = Flask(__name__)
    app.config.from_object(config[envv])

    api_bp = Blueprint('api', __name__)
    api = Api(api_bp)

    # Code for adding Flask RESTful resources goes here

    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(bp , url_prefix="/upload2")
    configure_uploads(app, photos)
    patch_request_class(app)
    app.jinja_env.block_start_string = '(%'  # 修改块开始符号
    app.jinja_env.block_end_string = '%)'  # 修改块结束符号
    app.jinja_env.variable_start_string = '(('  # 修改变量开始符号
    app.jinja_env.variable_end_string = '))'  # 修改变量结束符号
    app.jinja_env.comment_start_string = '(#'  # 修改注释开始符号
    app.jinja_env.comment_end_string = '#)'  # 修改注释结束符号
    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run()