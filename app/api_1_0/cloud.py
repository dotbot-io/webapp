from flask import Flask, current_app, g, jsonify
from flask_restful import Resource, Api

from flask_cors import CORS, cross_origin
from flask_json import as_json

from . import api

cors = CORS(api, resources={r"/": {"origins": "*"}})

@api.route('/discovery')
def test():
    #return {'name': current_app.config["ROS_MASTER_URI"], 'master': current_app.config["MASTER_URL"], 'ip': current_app.config["ROS_IP"]}
    return {'name': 'name', 'test': 'test'}
