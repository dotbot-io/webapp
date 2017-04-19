from datetime import datetime
from flask import render_template, session, redirect, url_for, request, Response

from . import ros

from ..models import Node, File
from .. import db


@ros.route('/')
def index():
	return render_template('ros/cover.html')
