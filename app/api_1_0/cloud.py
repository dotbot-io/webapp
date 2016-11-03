from flask import Flask, current_app, g
from flask_restful import Resource, Api

from flask_cors import CORS, cross_origin
from flask import jsonify

from . import api

restapi = Api(api)
cors = CORS(api, resources={r"/": {"origins": "*"}})

class Robot(Resource):
    decorators = [cross_origin(origin="*", headers=["content-type", "autorization"])]

    def get(self):
        return jsonify({'name': g.DOTBOT_NAME, 'master': g.MASTER_URL, 'ip': g.ROS_IP})

restapi.add_resource(Robot, '/discovery')
