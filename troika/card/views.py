# -*- coding: utf-8 -*-
import csv
import logging
import json
from grab import Grab

from flask import (Blueprint, abort, current_app, flash, render_template,
                   request, redirect)
from flask.ext.login import current_user, login_required

from troika.card.forms import CardForm
from troika.card.models import Card
from troika.history import tasks
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

    cards = Card.query.order_by('id desc').paginate(page, Card.PER_PAGE, False)
    return render_template("card/list.html",
                           cards=cards,
                           status_title=Card.STATUS_TITLE,
                           troika_state_title=Card.TROIKA_STATE_TITLE,
                           )


@blueprint.route("/", methods=['POST'])
@login_required
def search():
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        abort(404)

    search_data = {}
    query = Card.query
    for key in Card.SEARCH_KEYS:
        value = request.form.get(key)
        if value:
            search_data[key] = value
            query = query.filter(getattr(Card, key).like('%' + value + '%'))

    cards = query.order_by('id desc').paginate(page, Card.PER_PAGE, False)
    return render_template("card/list.html",
                           cards=cards,
                           status_title=Card.STATUS_TITLE,
                           troika_state_title=Card.TROIKA_STATE_TITLE,
                           search_data=search_data,)


@blueprint.route("/<int:card_id>", methods=['GET'])
@login_required
def show(card_id):

    card = Card.query.get(card_id)
    if not card:
        abort(404)

    spot_code = u'Не удалось связаться с API Mobispot'
    g = Grab()
    url = '%s/%s/%s' % (current_app.config.get('API_MOBISPOT'),
                        card.SPOT_URL, 
                        card.hard_id)
    g.setup(userpwd=current_app.config.get('AUTH_SIMPLE'))
    g.go(url)

    if g.response.code == 404:
        spot_code = u'N/A'

    if g.response.code == 200:
        response = json.loads(g.response.body)
        if 'code' in response:
            spot_code = response['code']

    return render_template("card/show.html",
                           card=card,
                           status_title=Card.STATUS_TITLE,
                           troika_state_title=Card.TROIKA_STATE_TITLE,
                           campus_title=card.get_campus_title(),
                           spot_code=spot_code)


@blueprint.route("/edit/<int:card_id>", methods=['GET', 'POST'])
@login_required
def edit(card_id):
    card = Card.query.get(card_id)
    if not card:
        abort(404)

    card.old_card = card.to_json()
    form = CardForm(request.form)
    if request.method == 'POST':
        form.id.data = card.id
        if form.validate():
            form.populate_obj(card)
            if card.save():
                flash(u'Данные успешно сохранены', "success")
        else:
            logger.debug('CARD EDIT')
            logger.debug('Request data: %(data)s' % {'data': request.form})
            logger.debug('Form error: %(error)s' %
                         {'error': format_error(form)})

            flash_errors(form)

    return render_template("card/edit.html",
                           card=card,
                           form=form,
                           status_title=card.get_status_title(),
                           troika_state_title=card.get_troika_state_title(),
                           campus_title=card.get_campus_title())


def allowed_file(filename):

    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config.get(
               'IMPORT_FILE_EXTENSIONS')


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
        if len(row) < 2:
            continue

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


@blueprint.route("/set_status", methods=['POST'])
@login_required
def set_status():
    card_list = []
    try:
        json_list = json.loads(request.form.get('selected_cards'))
        for item in json_list:
            if int(item) in card_list:
                continue
            card_list.append(int(item))
        troika_status = int(request.form.get('troika_status'))
        status = str(request.form.get('status'))
    except ValueError:
        abort(404)

    cards = Card.query.filter(Card.id.in_(card_list)).all()
    error = 'no'

    for card in cards:
        if troika_status != -1:
            card.troika_state = troika_status
        if status != '-1':
            card.status = status
        if not card.save():
            error = 'yes'

    if error == 'no':
        flash(u'Данные успешно сохранены', "success")

    return redirect("/card", code=303)
