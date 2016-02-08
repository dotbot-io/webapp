#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Sketch
from flask.ext.script import Manager, Shell, Command, Option
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, Sketch=Sketch)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
api.upgrade(app.config["SQLALCHEMY_DATABASE_URI"], app.config["SQLALCHEMY_MIGRATE_REPO"])
v = api.db_version(app.config["SQLALCHEMY_DATABASE_URI"], app.config["SQLALCHEMY_MIGRATE_REPO"])
print('Current database version: ' + str(v))

@manager.command
def test():
	"""Run the unit tests."""
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
	manager.run()
