from flask import Flask, current_app, g, jsonify
from flask_restful import Resource, Api

from flask_cors import CORS, cross_origin
from flask_json import as_json

from . import api

cors = CORS(api, resources={r"/": {"origins": "*"}})

@api.route('/rosnode/<path:node>/', methods=['DELETE'])
@as_json
def rostopic_kill(node):
    env = comp.env()
    env["ROS_NAMESPACE"] = '';
    print env
    subprocess.Popen(['rosnode', 'kill', node], env=env)
    return json_response( response='ok')
