from . import api
from ..models import Sketch
from .. import db
from flask import jsonify, request, flash, make_response, render_template
from flask_json import JsonError, json_response, as_json
from datetime import datetime

from sqlalchemy.exc import IntegrityError
import subprocess


@api.route('/bin/poweroff')
def poweroff():
	proc = subprocess.Popen(['sudo', 'poweoff'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return json_response( response='ok')

@api.route('/bin/update')
def update():
	proc = subprocess.Popen(['update_robotoma'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return json_response( response='ok')
