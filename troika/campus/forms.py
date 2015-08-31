# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import IntegerField, StringField, TextField
from wtforms.validators import DataRequired, Length

from .models import Campus


class CampusForm(Form):

    id = IntegerField()
    name = StringField(
        'Name',
        validators=[DataRequired(message=u'Поле обязательно для заполнения'),
                    Length(min=1, max=128)])
    address = StringField(
        'Address',
        validators=[DataRequired(message=u'Поле обязательно для заполнения'),
                    Length(min=3, max=128)])

    zip = StringField(
        'Zip',
        validators=[Length(min=0, max=16)])

    def __init__(self, *args, **kwargs):
        super(CampusForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(CampusForm, self).validate()
        if not initial_validation:
            return False

        return True
