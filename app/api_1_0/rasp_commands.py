from . import api
from ..models import Node
from .. import db
from flask import jsonify, request, flash, make_response, render_template, current_app
from flask_json import JsonError, json_response, as_json
from datetime import datetime

from sqlalchemy.exc import IntegrityError
import subprocess


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
	avahi_conf = render_template('code/avahi-deamon.conf', hostname=hostname)
	with open('/etc/avahi/avahi-daemon.conf', 'w') as f:
    	f.write(avahi_conf)

	return json_response( response='ok', newfile=avahi_conf)
