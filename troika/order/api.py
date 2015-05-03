# -*- coding: utf-8 -*-
import json
import logging

from flask import Blueprint, current_app, jsonify, make_response, request
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

logger = logging.getLogger(__name__)

blueprint = Blueprint("order_api", __name__, url_prefix='/api/order',
                      static_folder="../static")


@auth.get_password
def get_pw(username):
    users = current_app.config.get('API_USERS')
    if username in users:
        return users.get(username)
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)
