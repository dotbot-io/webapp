from flask import Blueprint
ros = Blueprint('ros', __name__)

from . import views
