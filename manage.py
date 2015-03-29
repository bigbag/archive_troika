#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os

from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager, Server, Shell

from troika.app import create_app
from troika.database import db
from troika.user.command import CreateUser
from troika.user.models import User

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

try:
    from troika.settings_local import Config
except Exception as e:
    logging.exception("Exception: %(body)s", {'body': e})
    from troika.settings import Config

app = create_app(Config)
manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}


manager.add_command('server', Server(host=app.config['APP_HOST'],
                                     port=app.config['APP_PORT']))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('create_user', CreateUser)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
