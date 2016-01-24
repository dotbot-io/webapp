from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class HostnameForm(Form):
	name = StringField("Enter the new Hostname", validators=[Required()])
	submit = SubmitField('Submit')