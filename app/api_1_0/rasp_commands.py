# -*- coding: utf-8 -*-


from . import api
from ..models import Node
from .. import db
from flask import jsonify, request, flash, make_response, render_template, current_app, redirect
from flask_json import JsonError, json_response, as_json
from datetime import datetime

from sqlalchemy.exc import IntegrityError
import subprocess
from flask import current_app


@api.route('/bin/poweroff')
def poweroff():
	proc = subprocess.Popen(['poweroff', 'now'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return json_response( response='ok')

@api.route('/bin/reboot')
def reboot():
	proc = subprocess.Popen(['reboot'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return json_response( response='ok')


@api.route('/bin/hostname/<hostname>')
def set_hostname(hostname):
	# proc = subprocess.Popen(['/usr/local/bin/change_hostname', hostname], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	# proc.wait()
	avahi_conf = render_template('configs/avahi-deamon.conf', hostname=hostname)
	with open('/etc/avahi/avahi-daemon.conf', 'w') as f:
		f.write(avahi_conf)

	name_conf = render_template('configs/name.bash', hostname=hostname)
	with open(current_app.config.get('DOTBOT_CONFIG_FOLDER') + '/name.bash', 'w') as f:
		f.write(name_conf)

	proc = subprocess.Popen(['service', 'avahi-daemon', 'restart'])
	proc.wait()
	return json_response( response='ok')
