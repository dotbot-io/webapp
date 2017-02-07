from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON
from config import config
from flask import g
from flask_cors import CORS

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
json = FlaskJSON()
cors = CORS(resources={r"/": {"origins": "*"}})


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    json.init_app(app)
    cors.init_app(app)

    from .api_1_0 import api as api_1_0_bp
    app.register_blueprint(api_1_0_bp, url_prefix='/api/v1.0')

    def get_ros():
        return '*', 'cloudbot','*/bridge'

    app.config["ROS_MASTER_URI"], app.config["DOTBOT_NAME"], app.config["ROS_IP"] = get_ros()
    @app.context_processor
    def utility_processor():
        g.MASTER_URL = app.config["ROS_MASTER_URI"]
        g.DOTBOT_NAME = app.config["DOTBOT_NAME"]
        g.ROS_IP = app.config["ROS_IP"]
    	return dict(version='cloud')

    return app
