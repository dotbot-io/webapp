from flask import Flask, current_app, g, jsonify, Response, request
from flask_restful import Resource, Api

from flask_cors import CORS, cross_origin
from flask_json import as_json
from flask_restful import Api, Resource, reqparse

from . import api
from compile import comp
from ..models import Node, File
from datetime import datetime
from .. import db


rest_api = Api(api)

class Robot(Resource):
    decorators = [cross_origin(origin="*", headers=["content-type", "autorization"], methods=['GET', 'PUT'])]
    def get(self):
        return jsonify({'name': current_app.config["DOTBOT_NAME"], 'master': current_app.config["ROS_MASTER_URI"], 'ip': current_app.config["ROS_IP"]})

class RobotSketch(Resource):
    decorators = [cross_origin()]

    def put(self):
        node_id = 29
        file_id = 53
    	f = File.query.get_or_404(file_id)
        parser = reqparse.RequestParser()
        parser.add_argument('code')
        args = parser.parse_args()

    	f.code = args['code']
    	f.last_edit = datetime.utcnow()
    	db.session.add(f)
    	f.save()
        db.session.commit()

    	n = Node.query.get_or_404(node_id)
    	comp.run(n)
    	return jsonify({'response': 'ok'})

    def get(self):
        return Response(comp.read_run_proc(node_id), mimetype='text/event-stream')




rest_api.add_resource(Robot, '/discovery')
rest_api.add_resource(RobotSketch, '/run/sketch')
