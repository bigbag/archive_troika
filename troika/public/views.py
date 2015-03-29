# -*- coding: utf-8 -*-
from flask import Blueprint, redirect, url_for
from flask.ext.login import current_user

blueprint = Blueprint('public', __name__, static_folder="../static")


@blueprint.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated():
        return redirect(url_for('card.list'))
    else:
        return redirect(url_for('user.login'))
