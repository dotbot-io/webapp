# -*- coding: utf-8 -*-

from flask import Flask, current_app
from flask_restful import Resource, Api, reqparse
import types

from . import api2

restfull_api = Api(api2)


def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper

restfull_api.route = types.MethodType(api_route, restfull_api)

@restfull_api.route('/hi')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@restfull_api.route('/hostname')
class Hostname(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('hostname')
        args = parser.parse_args()
        hostname = args['hostname']

    	avahi_conf = render_template('configs/avahi-deamon.conf', hostname=hostname)
    	with open('/etc/avahi/avahi-daemon.conf', 'w') as f:
    		f.write(avahi_conf)

    	name_conf = render_template('configs/name.bash', hostname=hostname)
    	with open(current_app.config.get('DOTBOT_CONFIG_FOLDER') + '/name.bash', 'w') as f:
    		f.write(name_conf)

    	proc = subprocess.Popen(['service', 'avahi-daemon', 'restart'])
    	proc.wait()


        return {'response': 'ok'}

@restfull_api.route('/ros_networking')
class Ros_Networking(Resource):
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('master')
        args = parser.parse_args()
        print args['master']

    	ros_conf = render_template('configs/config.bash', master=master)
    	with open(current_app.config.get('DOTBOT_CONFIG_FOLDER') + '/config.bash', 'w') as f:
    		f.write(ros_conf)

        return {'response': 'ok'}

    def get(self):
        return {'master': 'bla bla'} # TODO - add master
