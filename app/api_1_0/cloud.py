from flask import Flask, current_app, g, jsonify, Response, request, current_app, redirect, url_for
from flask_restful import Resource, Api

from flask_cors import CORS, cross_origin
from flask_json import JsonError, json_response, as_json
from flask_restful import Api, Resource, reqparse

from . import api
from ..models import Node, File
from datetime import datetime
from .. import db
import subprocess

from wifi import Cell, Scheme
from wifi.exceptions import ConnectionError
from compiler import Compiler

rest_api = Api(api)

comp = Compiler();


@api.before_request
def option_autoreply():
    if request.method == 'OPTIONS':
        resp = current_app.make_default_options_response()

        headers = None
        if 'ACCESS_CONTROL_REQUEST_HEADERS' in request.headers:
            headers = request.headers['ACCESS_CONTROL_REQUEST_HEADERS']

        h = resp.headers

        # Allow the origin which made the XHR
        h['Access-Control-Allow-Origin'] = '*'
        # Allow the actual method
        h['Access-Control-Allow-Methods'] = h['Allow']
        # Allow for 10 seconds
        h['Access-Control-Max-Age'] = 86400

        h["Access-Control-Allow-Credentials"] = False;
        h["Access-Control-Allow-Headers"] = "X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept";
        h["Access-Control-Allow-Content-Type"] = "text/event-stream; charset=utf-8"
        # We also keep current headers
        if headers is not None:
            h['Access-Control-Allow-Headers'] = headers

        return resp


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

    decorators = [cross_origin(origin='*')]

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code')
        args = parser.parse_args()

        '''
        node_id = 1
        file_id = 1
    	f = File.query.get_or_404(file_id)

    	f.code = args['code']
    	f.last_edit = datetime.utcnow()
    	db.session.add(f)
    	f.save()
        db.session.commit()

    	n = Node.query.get_or_404(node_id)
    	comp.run(n)
        print 'node running'
        '''
        of = open('/opt/virtualenvs/ros/project/dotbot_ws/src/dotbot_app/dotbot_ros_skeleton/node.py', "w")
        of.write(args['code'])
        of.close()
        comp.run_dotbot_node()
        print "pnods _out ", comp._pnodes
        return jsonify({'response': 'ok'})

    def get(self):
        print 'getting streaming'
        node_id = 1
        return redirect(url_for("api.stream", id=1))

    def options(self):
        pass

    def delete(self):
        print 'delete me'
        parser = reqparse.RequestParser()
        parser.add_argument('node')
        args = parser.parse_args()
        env = comp.env()
        env["ROS_NAMESPACE"] = '';
        killproc = subprocess.Popen(['rosnode', 'kill', args.node], env=env)
        killproc.wait()
    	return jsonify({'response': 'ok'})

class StreamNode(Resource):

    decorators = [cross_origin(origin='*')]

    def get(self, id):
        return Response(comp.read_run_proc(id), mimetype='text/event-stream')

class WifiCells(Resource):
    def get(self):
        cells = Cell.all('wlan0')
        wifi_info = []
        for c in cells:
            if c.ssid not in [wc['name'] for wc in wifi_info] + ["\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00"]:
                wifi_info.append({'name': c.ssid, 'encryption': c.encryption_type, 'encrypted': c.encrypted})
        return jsonify({'cells': wifi_info})

class WifiSchemes(Resource):
    def get(self):
        schemes = Scheme.all()
        return jsonify({'schemes': [s.__dict__ for s in schemes]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('password')
        args = parser.parse_args()

        schemes = [s for s in Scheme.all()]
        cells = Cell.all('wlan0')

        newscheme = None
        for cell in cells:
            if cell.ssid == args['name']:
                newscheme = Scheme.for_cell('wlan0', 'scheme-'+str(len(schemes)), cell, args['password'])
                break
        if newscheme is None:
            return jsonify({'response': "network non found"})
        else:
            newscheme.save()
            newscheme.activate()
            return jsonify({'response': "ok"})

class WifiScheme(Resource):
    def get(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('action')
        args = parser.parse_args()
        s = [s for s in Scheme.all() if s.name == name]
        if len(s) == 0:
            return jsonify({'response': "non found"})
        scheme = s[0]
        return jsonify({'scheme': scheme.__dict__})

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument('action')
        parser.add_argument('ssid')
        parser.add_argument('password')
        args = parser.parse_args()
        s = [s for s in Scheme.all() if s.name == name]
        if len(s) == 0:
            return jsonify({'response': "non found"})
        scheme = s[0]
        if args["action"] == 'connect':
            try:
                scheme.activate()
            except ConnectionError:
                return  jsonify({"error": "Failed to connect to %s." % scheme.name})
            return jsonify({'scheme': scheme.__dict__, "connected": True})
        elif args["action"] == "configure":
            cells = [cell for cell in Cell.all("wlan0") if cell.ssid == args['ssid']]
            if len(cells) == 0:
                return jsonify({'error': 'wifi not found'})
            sname = scheme.name

            for s in Scheme.all():
                s.delete()
                if s.name == sname:
                    s = Scheme.for_cell('wlan0', sname, cells[0], args['password'])
                s.save()
            return jsonify({'scheme': scheme.__dict__})
        elif args["action"] == "clean":
            sname = scheme.name
            for s in Scheme.all():
                s.delete()
                if s.name == sname:
                    s = Scheme('wlan0', sname)
                s.save()

        else:
            return jsonify({'scheme': scheme.__dict__})

    def delete(self, name):
        s = [s for s in Scheme.all() if s.name == name]
        if len(s) > 0:
            s[0].delete()
            return jsonify({'response': "ok"})
        else:
            return jsonify({'response': "non found"})




rest_api.add_resource(Robot, '/discovery')
rest_api.add_resource(RobotSketch, '/run/sketch')
rest_api.add_resource(StreamNode, '/stream/<int:id>', endpoint="stream")

rest_api.add_resource(WifiCells, '/wifi/cells')
rest_api.add_resource(WifiSchemes, '/wifi/schemes')
rest_api.add_resource(WifiScheme, '/wifi/schemes/<name>')
