import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    BOOTSTRAP_SERVE_LOCAL = True
    CATKIN_FOLDER = os.environ.get('CATKIN_FOLDER') or '/home/ubuntu/ros_ws'
    DOTBOT_PACKAGE_NAME = os.environ.get('DOTBOT_PACKAGE_NAME') or 'dotbot_app'
    ROS_ENVS = os.environ.get('ROS_ENVS') or '/opt/ros/kinetic/setup.bash'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////hbrain/run/data-dev.sqlite'

    @staticmethod
    def init_app(app):
        pass

config = {
    'default': DevelopmentConfig
}
