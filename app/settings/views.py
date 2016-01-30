from datetime import datetime
from flask import render_template, session, redirect, url_for, request
import subprocess

from . import settings
import socket

@settings.route('/', methods=['GET', 'POST'])
def settings():
    return render_template('settings/settings.html', hostname=socket.gethostname())
