# -*- coding: utf-8 -*-
from flask import flash


def format_error(form):

    result = []
    for field, errors in form.errors.items():
        for error in errors:
            label = getattr(form, field).label.text
            msg = "%(label)s - %(error)s" % {'label': label, 'error': error}
            result.append(msg)

    return ', '.join(result)


def flash_errors(form, category="warning"):

    for field, errors in form.errors.items():
        for error in errors:
            label = getattr(form, field).label.text
            msg = "%(label)s - %(error)s" % {'label': label, 'error': error}
            flash(msg, category)
