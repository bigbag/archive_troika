# -*- coding: utf-8 -*-
from flask import abort, Blueprint, flash, request, render_template
from flask.ext.login import login_required

from troika.card.models import Card
from troika.card.forms import CardForm
from troika.utils import flash_errors

blueprint = Blueprint("card", __name__, url_prefix='/card',
                      static_folder="../static")


@blueprint.route("/", methods=['GET'])
@blueprint.route("/<int:page>", methods=['GET'])
@login_required
def list(page=1):

    cards = Card.query.paginate(page, Card.CARDS_PER_PAGE, False)
    return render_template("card/list.html",
                           cards=cards,
                           status_title=Card.STATUS_TITLE,
                           troika_state_title=Card.TROIKA_STATE_TITLE)


@blueprint.route("/show/<int:card_id>", methods=['GET'])
@login_required
def show(card_id):

    card = Card.query.get(card_id)
    if not card:
        abort(404)

    return render_template("card/show.html",
                           card=card,
                           status_title=Card.STATUS_TITLE,
                           troika_state_title=Card.TROIKA_STATE_TITLE)


@blueprint.route("/edit/<int:card_id>", methods=['GET', 'POST'])
@login_required
def edit(card_id):

    card = Card.query.get(card_id)
    if not card:
        abort(404)

    form = CardForm(request.form)
    if request.method == 'POST':
        form.id.data = card.id
        if form.validate():
            form.populate_obj(card)
            card.save()
            flash(u'Данные успешно сохранены', "success")
        else:
            flash_errors(form)

    return render_template("card/edit.html",
                           card=card,
                           form=form,
                           status_title=Card.STATUS_TITLE,
                           troika_state_title=Card.TROIKA_STATE_TITLE)
