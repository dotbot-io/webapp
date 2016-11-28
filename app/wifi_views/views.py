from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import wifi_views

@wifi_views.route("/scan")
def wifi_scan():
    return render_template('wifi/scan.html')
