from datetime import datetime
from flask import render_template, session, redirect, url_for, request, Response

from . import ros

from ..models import Sketch
from .. import db


@ros.route('/')
def index():
	return render_template('ros/cover.html')

@ros.route('/edit/<int:id>')
def edit(id):
	s = Sketch.query.get_or_404(id)
	return render_template('ros/edit.html', sketch=s)

@ros.route('/programs')
def sketches():
    return render_template('ros/programs.html', current_time=datetime.utcnow())

@ros.route('/rosnodes')
def rosnodes():
    return render_template('ros/rosnodes.html', current_time=datetime.utcnow())

@ros.route('/rostopics')
def rostopics():
    return render_template('ros/rostopics.html', current_time=datetime.utcnow())

@ros.route('/test')
def test_page():
    return render_template('ros/test.html')

@ros.route('/joy')
def joy_page():
    return render_template('ros/joystick.html')
