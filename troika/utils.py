# -*- coding: utf-8 -*-
'''Helper utilities and decorators.'''
from flask import flash


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            label = getattr(form, field).label.text
            msg = "%(label)s - %(error)s" % {'label': label, 'error': error}
            flash(msg, category)
