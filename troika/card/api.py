# -*- coding: utf-8 -*-
import json

from flask import (Blueprint, abort, current_app, flash, jsonify,
                   make_response, render_template, request)
from flask.ext.httpauth import HTTPDigestAuth

from troika.card.models import Card
from troika.helpers.header_helper import json_headers

blueprint = Blueprint("card_api", __name__, url_prefix='/api/card',
                      static_folder="../static")

auth = HTTPDigestAuth()


@auth.get_password
def get_pw(username):
    users = current_app.config.get('API_USERS')
    if username in users:
        return users.get(username)
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@blueprint.route("/", methods=['GET'])
@auth.login_required
@json_headers
def get_activation():
    cards = Card.query.limit(10).all()
    result = []
    for card in cards:
        result.append(card.to_dict())

    return make_response(json.dumps(result), 200)


@blueprint.route("/free", methods=['GET'])
@auth.login_required
@json_headers
def get_new():
    cards = Card.query.filter_by(status=Card.STATUS_NEW).limit(10).all()
    result = []
    for card in cards:
        result.append(card.to_dict())

    return make_response(json.dumps(result), 200)
