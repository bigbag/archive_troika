# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired


class OrderForm(Form):

    id = IntegerField()
    user_id = IntegerField('Mobispot user id', validators=[DataRequired()])
    user_email = StringField('Mobispot user email', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

    def validate_csrf_token(self, field):
        pass
