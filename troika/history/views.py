# -*- coding: utf-8 -*-
import logging

from flask import Blueprint, abort, render_template, request
from flask.ext.login import login_required

from troika.card.models import Card
from troika.history.models import CardsHistory

logger = logging.getLogger(__name__)

blueprint = Blueprint("history", __name__, url_prefix='/history',
                      static_folder="../static")


@blueprint.route("/", methods=['GET'])
@login_required
def list():

    try:
        page = int(request.args.get('page', 1))
        card_id = int(request.args.get('card_id', 0))
    except ValueError:
        abort(404)

    card = None
    query = CardsHistory.query.order_by('action_date desc')
    if card_id:
        card = Card.query.get(card_id)
        if not card:
            abort(404)

        query = query.filter_by(card_id=card_id)
    history = query.paginate(page, CardsHistory.PER_PAGE, False)
    return render_template("history/list.html",
                           card=card,
                           history=history,
                           action_title=CardsHistory.ACTION_TITLE,
                           card_id=card_id)


@blueprint.route("/<int:history_id>", methods=['GET'])
@login_required
def show(history_id):

    history = CardsHistory.query.get(history_id)
    if not history:
        abort(404)

    return render_template("history/show.html",
                           history=history,
                           to_text=CardsHistory.to_text,
                           action_title=CardsHistory.ACTION_TITLE)
