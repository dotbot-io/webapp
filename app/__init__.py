from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask_json import FlaskJSON
from config import config
from flask import g


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

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    from .settings import settings as settings_bp
    app.register_blueprint(settings_bp, url_prefix='/settings')


    from .ros import ros as ros_bp
    app.register_blueprint(ros_bp)

    from .gui import gui as gui_bp
    app.register_blueprint(gui_bp, url_prefix="/gui")

    from .api_1_0 import api as api_1_0_bp
    app.register_blueprint(api_1_0_bp, url_prefix='/api/v1.0')



    def get_version():
        import subprocess, os
        path = os.path.realpath(__file__)
        p = subprocess.Popen('git describe --always', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=os.path.dirname(path))
        ver = ""
        for line in p.stdout.readlines():
            ver =  line.rstrip()
        retval = p.wait()
        return ver

    def get_ros():
        import json, subprocess
        source = 'source ' + app.config["ROS_ENVS"]
        dump = 'python -c "import os, json;print json.dumps(dict(os.environ))"'
        pipe = subprocess.Popen(['/bin/bash', '-c', '%s && %s' %(source,dump)], stdout=subprocess.PIPE)
        env_info =  pipe.stdout.read()
        print env_info
        env = json.loads(env_info)
        return env["ROS_MASTER_URI"].split('//')[1].split(":")[0] or 'localhost', env["DOTBOT_NAME"] or 'dotbot', env["ROS_IP"] or 'localhost'

    app.config["ROS_MASTER_URI"], app.config["DOTBOT_NAME"], app.config["ROS_IP"] = get_ros()
    @app.context_processor
    def utility_processor():
        g.MASTER_URL = app.config["ROS_MASTER_URI"]
        g.DOTBOT_NAME = app.config["DOTBOT_NAME"]
        g.ROS_IP = app.config["ROS_IP"]
    	return dict(version=get_version())

    return app
