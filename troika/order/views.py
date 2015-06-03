# -*- coding: utf-8 -*-
import logging

from flask import (Blueprint, abort, current_app, flash, render_template,
                   request)
from flask.ext.login import login_required

from troika.order.models import Order

logger = logging.getLogger(__name__)

blueprint = Blueprint("order", __name__, url_prefix='/order',
                      static_folder="../static")


@blueprint.route("/", methods=['GET'])
@login_required
def list():

    try:
        page = int(request.args.get('page', 1))
    except ValueError:
        abort(404)

    query = Order.query.order_by('creation_date desc')

    orders = query.paginate(page, Order.PER_PAGE, False)
    return render_template("order/list.html",
                           orders=orders,
                           status_title=Order.STATUS_TITLE)


@blueprint.route("/<int:order_id>", methods=['GET'])
@login_required
def show(order_id):

    order = Order.query.get(order_id)
    if not order:
        abort(404)

    return render_template("order/show.html",
                           order=order,
                           status_title=Order.STATUS_TITLE)
