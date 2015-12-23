from . import api
from flask import jsonify, request, flash, render_template
from flask_json import JsonError, json_response, as_json
from datetime import datetime
import subprocess

from sqlalchemy.exc import IntegrityError


@api.route('/rostopics/')
@as_json
def rostopic():
    p = subprocess.Popen('rostopic list', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    topics = []
    info = []
    for line in p.stdout.readlines():
        topics.append([line])
    for i in range(0, len(topics)):
        pt = subprocess.Popen('rostopic info '  + topics[i][0], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in pt.stdout.readlines():
            topics[i].append(line.split(':')[1])
            break
    return jsonify(topics=topics)

@api.route('/rosnodes/')
@as_json
def rosnode():
    p = subprocess.Popen('rosnode list', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    nodes = []
    for line in p.stdout.readlines():
        nodes.append([line[1:-1] ])
    return jsonify(nodes=nodes)

@api.route('/rosnode/<node>/', methods=['DELETE'])
@as_json
def rostopic_kill(node):
	subprocess.Popen(['rosnode', 'kill', node])
	return json_response( response='ok')


'''
@api.route('/nodes/')
@as_json
def get_nodes():
	sketches = Sketch.query.all()
	return dict(sketches=[s.to_json() for s in sketches])


@api.route('/sketches/<int:id>')
@as_json
def get_sketch(id):
	s = Sketch.query.get_or_404(id)
	return s.to_json()

@api.route('/sketches/', methods=['POST'])
@as_json
def post_sketch():
	print 'request:', request.json
	s = Sketch.from_json(request.json)
	db.session.add(s)
	try:
		db.session.commit()
	except IntegrityError:
		db.session.rollback()
		flash('Title already in Database')
		raise JsonError(error='Title already in Database')
	return json_response( response='ok')

	

@api.route('/sketches/<int:id>/', methods=['DELETE'])
@as_json
def delete_sketch(id):
	s = Sketch.query.filter_by(id=id).first()
	if s is not None:
		db.session.delete(s)
		db.session.commit()
		return json_response(response='ok')
	raise JsonError(error='sketch not in database')

@api.route('/sketches/', methods=['DELETE'])
@as_json
def delete_all_sketches():
	Sketch.query.delete()
	db.session.commit()
	return json_response(response='ok')
	


@api.route('/sketches/<int:id>/', methods=['PUT'])
@as_json
def put_sketch(id):
	s = Sketch.query.get_or_404(id)
	s.code = request.json.get('code', s.code)
	s.last_edit = datetime.utcnow()
	db.session.add(s)
	return json_response(response='ok')

'''
