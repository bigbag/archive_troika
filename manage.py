#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from flask.ext.migrate import MigrateCommand
from flask.ext.script import Manager, Server, Shell

from troika.app import create_app
from troika.card.command import AddCard
from troika.card.models import Card
from troika.database import db
from troika.user.command import AddUser
from troika.user.models import User

try:
    from troika.settings_local import Config
except Exception as e:
    logging.exception("Exception: %(body)s", {'body': e})
    from troika.settings import Config

app, celery = create_app(Config)
manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User, 'Card': Card}


manager.add_command('server', Server(host=app.config['APP_HOST'],
                                     port=app.config['APP_PORT']))
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('add_user', AddUser)
manager.add_command('add_card', AddCard)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
