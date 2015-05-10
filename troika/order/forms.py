# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import IntegerField, StringField
from wtforms.validators import DataRequired


class OrderForm(Form):

    id = IntegerField()
    mobispot_user_id = IntegerField(
        'Mobispot user id',
        validators=[DataRequired(message=u'Поле обязательно для заполнения'), ])
    mobispot_user_email = StringField(
        'Mobispot user email',
        validators=[DataRequired(message=u'Поле обязательно для заполнения'), ])

    status = StringField(u'Статус')

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
