from flask import Flask, current_app, g, jsonify
from flask_restful import Resource, Api

from flask_cors import CORS, cross_origin
from flask_json import as_json

from . import api


rest_api = Api(api)

class Robot(Resource):
    decorators = [cross_origin(origin="*", headers=["content-type", "autorization"])]
    def get(self):
        return jsonify({'name': current_app.config["DOTBOT_NAME"], 'master': current_app.config["ROS_MASTER_URI"], 'ip': current_app.config["ROS_IP"]})




rest_api.add_resource(Robot, '/discovery')
