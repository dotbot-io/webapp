from flask import Flask, current_app, g, jsonify
from flask_restful import Resource, Api

from flask_cors import CORS, cross_origin
from flask_json import as_json

from . import api

cors = CORS(api, resources={r"/": {"origins": "*"}})

@api.route('/test')
def test():
    return {'name': g.DOTBOT_NAME, 'master': g.MASTER_URL, 'ip': g.ROS_IP}

@api.route("/discovery")
@as_json
def discovery():
    return 'test'
