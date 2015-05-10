# -*- coding: utf-8 -*-
import json
import logging

from flask import Blueprint, current_app, jsonify, make_response, request
from flask.ext.httpauth import HTTPBasicAuth

from troika.card.models import Card
from troika.order.models import Order
from troika.helpers.header_helper import json_headers

auth = HTTPBasicAuth()

logger = logging.getLogger(__name__)

blueprint = Blueprint("card_api", __name__, url_prefix='/api/card',
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


@blueprint.route("/", methods=['GET'])
@auth.login_required
@json_headers
def get_all():
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


@blueprint.route("/release", methods=['POST'])
@auth.login_required
@json_headers
def release_card():
    logger.debug('API CARD RELEASE')
    logger.debug('Request data: %(data)s' % {'data': request.form})

    hard_id = request.form.get('hard_id')
    if not hard_id:
        return make_response(jsonify({'error': 'Not valid request'}), 400)

    order = Order.query.filter_by(status=Order.STATUS_NEW).first()
    if not order:
        return make_response(jsonify({'error': 'Not found new order'}), 404)

    card = Card().get_new_and_active(hard_id)
    if not card:
        return make_response(jsonify({'error': 'Not found card'}), 404)

    order.status = Order.STATUS_COMPLETED
    order.save()

    card.old_card = card.to_json()
    card.status = Card.STATUS_INPROGRESS
    card.order_id = order.id
    card.save()

    return make_response(json.dumps({'card_id': card.id,
                                     'user_id': order.user_id}), 200)


@blueprint.route("/hard_id/<hard_id>", methods=['GET'])
@auth.login_required
@json_headers
def get_by_hard_id(hard_id):
    card = Card.query.filter_by(hard_id=hard_id).first()
    if not card:
        return make_response(jsonify({'error': 'Not found'}), 404)

    return make_response(json.dumps(card.to_dict()), 200)


@blueprint.route("/hard_id/<hard_id>", methods=['POST'])
@auth.login_required
@json_headers
def update(hard_id):
    logger.debug('API CARD UPDATE')
    logger.debug('Request data: %(data)s' % {'data': request.form})

    troika_state = request.form.get('troika_state')
    status = request.form.get('status')
    if not troika_state and not status:
        return make_response(jsonify({'error': 'Bad request'}), 400)

    if status and status not in Card.STATUS_TITLE:
        return make_response(jsonify({'error': 'Bad request'}), 400)

    if troika_state and int(troika_state) not in Card.TROIKA_STATE_TITLE:
        return make_response(jsonify({'error': 'Bad request'}), 400)

    card = Card.query.filter_by(hard_id=hard_id).first()
    if not card:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if troika_state:
        card.troika_state = troika_state

    card.old_card = card.to_json()
    if status:
        card.status = status
    card.save()

    return make_response(json.dumps({}), 200)
