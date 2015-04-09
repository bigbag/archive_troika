# -*- coding: utf-8 -*-
import copy
import csv
import logging

from flask import (Blueprint, abort, current_app, flash, render_template,
                   request)
from flask.ext.login import current_user, login_required

from troika.card import tasks
from troika.card.forms import CardForm
from troika.card.models import Card
from troika.utils import flash_errors, format_error

logger = logging.getLogger(__name__)

blueprint = Blueprint("card", __name__, url_prefix='/card',
                      static_folder="../static")


@blueprint.route("/", methods=['GET'])
@login_required
def list():

    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        abort(404)

    cards = Card.query.paginate(page, Card.PER_PAGE, False)
    return render_template("card/list.html",
                           cards=cards,
                           status_title=Card.STATUS_TITLE,
                           troika_state_title=Card.TROIKA_STATE_TITLE)


@blueprint.route("/<int:card_id>", methods=['GET'])
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

    card_old = copy.deepcopy(card)
    form = CardForm(request.form)
    if request.method == 'POST':
        form.id.data = card.id
        if form.validate():
            form.populate_obj(card)
            if card.save():
                tasks.update_action.delay(
                    current_user.id, card.id, card_old.to_json(), card.to_json())
                flash(u'Данные успешно сохранены', "success")
        else:
            logger.debug('CARD EDIT')
            logger.debug('Request data: %(data)s' % {'data': request.form})
            logger.debug('Form error: %(error)s' % {'error': format_error(form)})

            flash_errors(form)

    return render_template("card/edit.html",
                           card=card,
                           form=form,
                           status_title=Card.STATUS_TITLE,
                           troika_state_title=Card.TROIKA_STATE_TITLE)


def allowed_file(filename):

    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config.get('IMPORT_FILE_EXTENSIONS')


def parsing_csv(file):

    csvfile = file.stream.read()
    try:
        dialect = csv.Sniffer().sniff(csvfile)
    except:
        flash(u'Загруженный файл имеет неверный формат.', 'danger')
        return

    cards = []
    reader = csv.reader(csvfile.split('\n'), dialect)
    for row in reader:
        card = Card(row[0], row[1])
        old_card = Card.query.filter(
            (Card.hard_id == card.hard_id) |
            (Card.troika_id == card.troika_id)).first()
        if old_card:
            continue
        cards.append(row)

    return cards


@blueprint.route("/import", methods=['GET', 'POST'])
@login_required
def import_cards():

    if request.method == 'POST':
        file = request.files['importFile']
        if file and allowed_file(file.filename):
            cards = parsing_csv(file)
            if not cards:
                flash(u'Загруженный файл не содержит новых карт.', 'danger')
            else:
                for row in cards:
                    card = Card(row[0], row[1])
                    card.save()

                    tasks.create_action.delay(
                        current_user.id, card.id, card.to_json())

                flash(u'Данные успешно загружены', 'success')

    return render_template("card/import.html")
