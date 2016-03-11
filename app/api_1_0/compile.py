from . import api
from ..models import Node
from compiler import Compiler

from flask_json import JsonError, json_response
from flask import Response, request

comp = Compiler();


@api.route('/catkin')
def catkin():
    comp.catkin()
    return Response(comp.read_buid_proc(id), mimetype='text/event-stream')

@api.route('/nodes/<int:id>/build')
def build(id):
    n = Node.query.get_or_404(id)
    comp.compile(n)
    return Response(comp.read_buid_proc(id), mimetype='text/event-stream')

@api.route('/nodes/<int:id>/run')
def run_node(id):
    comp.run(id)
    return Response(comp.read_run_proc(id), mimetype='text/event-stream')
