# -*- coding: utf-8 -*-
import logging

from flask import Flask, render_template

from troika import card, public, user, history
from troika.assets import assets
from troika.extensions import (bcrypt, cache, celery, db, debug_toolbar,
                               login_manager, migrate)

try:
    from troika.settings_local import Config
except Exception as e:
    logging.exception("Exception: %(body)s", {'body': e})
    from troika.settings import Config


def create_app(config_object=Config):

    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):

    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    celery.init_app(app)
    return None


def register_blueprints(app):

    app.register_blueprint(card.views.blueprint)
    app.register_blueprint(card.api.blueprint)

    app.register_blueprint(history.views.blueprint)
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("errors/{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 405, 500]:
        app.errorhandler(errcode)(render_error)
    return None
