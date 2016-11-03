from flask import Flask, current_app, g
from flask_restful import Resource, Api

from flask_cors import CORS, cross_origin
from flask import jsonify

from . import api

cors = CORS(api, resources={r"/": {"origins": "*"}})

@api.route('/test')
def test():
    return 'test'

@api.route("/discovery")
def discovery():
    return jsonify({'name': g.DOTBOT_NAME, 'master': g.MASTER_URL, 'ip': g.ROS_IP})
