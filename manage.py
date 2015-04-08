#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from flask.ext.migrate import MigrateCommand
from flask.ext.script import Command, Manager, Server, Shell

from celery.app.log import Logging
from celery.bin.celery import main as celery_main
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

app = create_app(Config)
manager = Manager(app)


class StartCelery(Command):

    def run(self, **args):
        Logging._setup = True
        celery_args = ['celery', 'worker', '-B', '-s', '/tmp/celery.db', '--concurrency=2']
        with app.app_context():
            return celery_main(celery_args)


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
manager.add_command('start_celery', StartCelery)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
