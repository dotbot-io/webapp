from datetime import datetime
from flask import render_template, session, redirect, url_for, request

from . import settings
from forms import HostnameForm
# from .forms import NameForm 
# from .. import db
# from ..models import User

@settings.route('/', methods=['GET', 'POST'])
def settings():
    form = HostnameForm(request.form)
    if request.method == 'POST' and form.validate():
        proc = subprocess.Popen(['/usr/local/bin/change_hostname', form.name.data], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return render_template('settings/settings.html', form=form)