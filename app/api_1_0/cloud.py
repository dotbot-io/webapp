from flask import Flask, current_app, g, jsonify
from flask_restful import Resource, Api

from flask_cors import CORS, cross_origin
from flask_json import as_json

from . import api

cors = CORS(api, resources={r"/": {"origins": "*"}})

rest_api = Api(api)

class Robot(Resource):
    def get(self):
        return jsonify({'name': current_app.config["DOTBOT_NAME"], 'master': current_app.config["ROS_MASTER_URI"], 'test': current_app.config["ROS_IP"]})

rest_api.add_resource(Robot, '/rest/discovery')


@api.route('/discovery')
def test():
    #return {'name': current_app.config["ROS_MASTER_URI"], 'master': current_app.config["MASTER_URL"], 'ip': current_app.config["ROS_IP"]}
    return jsonify({'name': current_app.config["DOTBOT_NAME"], 'master': current_app.config["ROS_MASTER_URI"], 'test': current_app.config["ROS_IP"]})
