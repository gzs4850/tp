from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from config import config

db = SQLAlchemy()
scheduler = APScheduler()

def create_app(config_name):
    app = Flask(__name__)
    # 进行app配置，导入config
    app.config.from_object(config[config_name])
    # 初始化app配置
    config[config_name].init_app(app)

    db.init_app(app)

    # 初始化apscheduler
    scheduler.init_app(app)
    scheduler.start()

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')


    return app
