# -*- coding: utf-8 -*-
import os
from flask import Flask
from app.main import main


def create_app(config_filename):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    app.config.from_object(config_filename)

    # 配置蓝本
    app.register_blueprint(main)

    return app
