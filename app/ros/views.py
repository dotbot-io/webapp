from datetime import datetime
from flask import render_template, session, redirect, url_for, request, Response

from . import ros

from ..models import Node, File
from .. import db


@ros.route('/')
def index():
	return render_template('ros/cover.html')

@ros.route('/file/edit/<int:id>')
def edit_file(id):
	s = File.query.get_or_404(id)
	return render_template('ros/edit.html', file=s)

@ros.route('/nodes')
def nodes():
    return render_template('ros/nodes.html', current_time=datetime.utcnow())

@ros.route('/nodes/<int:id>')
def files_of_node(id):
    return render_template('ros/files.html', current_time=datetime.utcnow(), node_id = id)


@ros.route('/rosnodes')
def rosnodes():
    return render_template('ros/rosnodes.html', current_time=datetime.utcnow())

@ros.route('/rostopics')
def rostopics():
    return render_template('ros/rostopics.html', current_time=datetime.utcnow())

@ros.route('/rosconsole')
def rosconsole():
    return render_template('ros/rosconsole.html', current_time=datetime.utcnow())


@ros.route('/test')
def test_page():
    return render_template('ros/test.html')

@ros.route('/play')
def play_page():
    return render_template('ros/moves.html')


@ros.route('/joy')
def joy_page():
    return render_template('ros/joystick.html')
