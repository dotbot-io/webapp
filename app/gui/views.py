from datetime import datetime
from flask import render_template, session, redirect, url_for, request, Response

from . import gui



@gui.route('/simple_ctrl')
def play_page():
    return render_template('gui/simple_ctrl.html')
