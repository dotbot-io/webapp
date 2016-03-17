from . import db
from datetime import datetime
from os import path, mkdir, chmod
import stat
import os
from flask import current_app, render_template

class File(db.Model):
	__tablename__ = "file"

	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(128), unique=True, index=True)
	last_edit = db.Column(db.DateTime, default=datetime.utcnow)
	code = db.Column(db.Text, default="")
	node_id = db.Column(db.Integer, db.ForeignKey('nodes.id'))
	is_executable = db.Column(db.Boolean, default=False)

	def language(self):
		return self.filename.split('.')[-1]

	def __repr__(self):
		return '<File %r>' % self.filename

	def save(self):
		of = open(self.filename, "w")
		of.write(self.code)
		of.close()
		if self.is_executable == True:
			chmod(self.filename, stat.S_IRWXU)


	def delete(self):
		os.remove(self.filename)
		db.session.delete(self)
		db.session.commit()


	def to_json(self):
		json_file = {
			'id' : self.id,
			'filename' : path.basename(self.filename),
			'last_edit' : self.last_edit,
			'node_id' : self.node_id
		}
		return json_file

	@staticmethod
	def from_json(json_file):
		filename = json_file.get('filename')
		code = json_file.get('code')
		return File(filename=filename, code=code)


class Node(db.Model):
	__tablename__ = 'nodes'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True, index=True)
	files = db.relationship('File', backref='node')
	created = db.Column(db.DateTime, default=datetime.utcnow)
	catkin_initialized = db.Column(db.Boolean, default=False)
	language = db.Column(db.String(8), default='cpp')

	def create(self):
		if not self.exist():
			mkdir(self._folder());
			if self.language == 'cpp':
				main_file = File(filename=path.join(self._folder(), 'node.' + self.language), node = self)
				main_file.code = render_template('code/default.cpp')
			else:
				main_file = File(filename=path.join(self._folder(), 'node_' + str(self.id) + '.' + self.language), node=self, is_executable=True)
				main_file.code = render_template('code/default.py')

			dotbot_file = File(filename=path.join(self._folder(), '.dotbot_ros'), node = self)
			db.session.add(main_file,dotbot_file)
			db.session.commit()
			main_file.save()
			dotbot_file.save()

	def exist(self):
		return path.isdir(self._folder())

	def _folder(self):
		if self.language == 'cpp':
			return path.join(current_app.config["CATKIN_FOLDER"], 'src', current_app.config["DOTBOT_PACKAGE_NAME"], 'src_' + str(self.id))
		else:
			return path.join(current_app.config["CATKIN_FOLDER"], 'src', current_app.config["DOTBOT_PACKAGE_NAME"], 'script_' + str(self.id))

	def executable(self):
		if self.language == 'cpp':
			return 'src_' + str(id) + '_' + current_app.config["DOTBOT_PACKAGE_NAME"]+'_node'
		else:
			return 'node_' + str(self.id) + '.' + self.language

	def __repr__(self):
		return '<Node %r>' % self.title

	@staticmethod
	def from_json(json_node):
		title = json_node.get('title')
		language = json_node.get('language') or 'cpp'
		return Node(name=title, language=language)

	def to_json(self):
		json_node = {
			'id' : self.id,
			'name' : self.name,
			'created' : self.created,
			'files_cnt' : len(self.files),
			'language' : self.language
		}
		return json_node
