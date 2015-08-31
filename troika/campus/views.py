# -*- coding: utf-8 -*-
import logging

from flask import (Blueprint, abort, current_app, flash, render_template,
                   request, redirect)
from flask.ext.login import login_required

from troika.campus.models import Campus
from troika.campus.forms import CampusForm

from troika.utils import flash_errors, format_error

logger = logging.getLogger(__name__)

blueprint = Blueprint("campus", __name__, url_prefix='/campus',
                      static_folder="../static")


@blueprint.route("/", methods=['GET'])
@login_required
def list():
    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        abort(404)

    query = Campus.query.order_by('id')

    campuses = query.paginate(page, Campus.PER_PAGE, False)
    return render_template("campus/list.html",
                           campuses=campuses)


@blueprint.route("/new", methods=['GET', 'POST'])
@login_required
def new():

    form = CampusForm(request.form)
    if request.method == 'POST':
        if form.validate():
            campus = Campus()
            form.populate_obj(campus)
            if campus.save():
                flash(u'Данные успешно сохранены', "success")
                return redirect("/campus", code=303)
        else:
            flash_errors(form)

    return render_template("campus/new.html", form=form, campus=form.data)


@blueprint.route("/edit/<int:campus_id>", methods=['GET', 'POST'])
@login_required
def edit(campus_id):

    campus = Campus.query.get(campus_id)
    if not campus:
        abort(404)

    form = CampusForm(request.form)
    if request.method == 'POST':
        form.id.data = campus.id
        if form.validate():
            form.populate_obj(campus)
            if campus.save():
                flash(u'Данные успешно сохранены', "success")
        else:
            flash_errors(form)

    return render_template("campus/edit.html",
                           campus=campus,
                           form=form)


@blueprint.route("/remove/<int:campus_id>", methods=['GET', 'POST'])
@login_required
def remove(campus_id):

    campus = Campus.query.get(campus_id)
    if not campus:
        abort(404)

    if request.method == 'POST':
        id = campus.id
        name = campus.name
        campus.delete()
        flash(u'Кампус %s %s удален' % (id, name), "success")
        return redirect("/campus", code=303)

    return render_template("campus/remove.html", campus=campus)
