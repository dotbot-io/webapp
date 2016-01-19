from datetime import datetime
from flask import render_template, session, redirect, url_for, request, Response

from . import ardu

from ..models import Sketch
from .. import db


@ardu.route('/') 
def index():
	return render_template('ardu/cover.html')

@ardu.route('/edit/<int:id>') 
def edit(id):
	s = Sketch.query.get_or_404(id)
	return render_template('ardu/arduino.html', sketch=s)


@ardu.route('/programs') 
def sketches():
    return render_template('ardu/sketches.html', current_time=datetime.utcnow())

@ardu.route('/monitor') 
def monitor():
    return render_template('ardu/monitor.html')

@ardu.route('/rosnodes') 
def rosnodes():
    return render_template('ardu/rosnodes.html', current_time=datetime.utcnow())

@ardu.route('/rostopics') 
def rostopics():
    return render_template('ardu/rostopics.html', current_time=datetime.utcnow())
