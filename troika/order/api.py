# -*- coding: utf-8 -*-
import json
import logging

from flask import abort, Blueprint, current_app, jsonify, make_response, request
from flask.ext.httpauth import HTTPBasicAuth

from troika.order.models import Order
from troika.order.forms import OrderForm

from troika.helpers.header_helper import json_headers
from troika.utils import format_error

auth = HTTPBasicAuth()

logger = logging.getLogger(__name__)

blueprint = Blueprint("order_api", __name__, url_prefix='/api/order',
                      static_folder="../static")


@auth.get_password
def get_pw(username):
    users = current_app.config.get('API_USERS')
    if not users:
        return None

    api_users = users.get(blueprint.name)
    if username in api_users:
        return api_users.get(username)
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@blueprint.route("/", methods=['POST'])
@auth.login_required
@json_headers
def create():

    form = OrderForm(request.form)
    if form.validate():
        order = Order()
        form.populate_obj(order)
        if not order.save():
            return make_response(json.dumps({'error': 'Duplicate entry'}), 400)

        return make_response(json.dumps({'id': order.id}), 201)
    else:
        logger.debug('API ORDER CREATE')
        logger.debug('Request data: %(data)s' % {'data': request.form})
        logger.debug('Form error: %(error)s' % {'error': format_error(form)})

        return make_response(json.dumps({'error': form.errors}), 400)
