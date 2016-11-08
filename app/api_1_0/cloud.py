from flask import Flask, current_app, g, jsonify, Response, request
from flask_restful import Resource, Api

from flask_cors import CORS, cross_origin
from flask_json import JsonError, json_response, as_json
from flask_restful import Api, Resource, reqparse

from . import api
from compile import comp
from ..models import Node, File
from datetime import datetime
from .. import db
import subprocess


rest_api = Api(api)

def getMAC(interface):
    try:
        str = open('/sys/class/net/' + interface + '/address').read()
    except:
        str = "00:00:00:00:00:00"
    return str[0:17]

class Robot(Resource):
    decorators = [cross_origin(origin="*", headers=["content-type", "autorization"], methods=['GET', 'PUT'])]
    def get(self):
        return jsonify({'name': current_app.config["DOTBOT_NAME"], 'master': current_app.config["ROS_MASTER_URI"], 'ip': current_app.config["ROS_IP"], "macaddress":getMAC('wlan0'), "model":"dotbot-ros b0.5"})

class RobotSketch(Resource):
    decorators = [cross_origin()]

    def put(self):
        node_id = 27
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
        node_id = 27
        return Response(comp.read_run_proc(node_id), mimetype='text/event-stream')

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('node')
        args = parser.parse_args()
        env = comp.env()
        env["ROS_NAMESPACE"] = '';
        print env
        subprocess.Popen(['rosnode', 'kill', args.node], env=env)
    	return jsonify({'response': 'ok'})



rest_api.add_resource(Robot, '/discovery')
rest_api.add_resource(RobotSketch, '/run/sketch')


@api.route('/rosnode_kill/<path:node>', methods=['DELETE'])
@as_json
@cross_origin(origin="*", headers=["content-type", "autorization"], methods=['GET', 'PUT', 'DELETE'])
def rosnode_kill(node):
    env = comp.env()
    env["ROS_NAMESPACE"] = '';
    print env
    subprocess.Popen(['rosnode', 'kill', node], env=env)
    return json_response( response='ok')
