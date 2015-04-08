# -*- coding: utf-8 -*-
from flask.ext.bcrypt import Bcrypt
from flask.ext.cache import Cache
from flask.ext.celery import Celery
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()

login_manager = LoginManager()

db = SQLAlchemy()

migrate = Migrate()

cache = Cache()

celery = Celery()

debug_toolbar = DebugToolbarExtension()
