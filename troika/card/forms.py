# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import IntegerField, StringField, TextField
from wtforms.validators import DataRequired, Length

from .models import Card


class CardForm(Form):

    id = IntegerField()
    hard_id = StringField(
        'Hard ID',
        validators=[DataRequired(message=u'Поле обязательно для заполнения'),
                    Length(min=3, max=128)])
    troika_id = StringField(
        'Troika ID',
        validators=[DataRequired(message=u'Поле обязательно для заполнения'),
                    Length(min=3, max=128)])
    name_ru = TextField(u'Название на русском', validators=[Length(min=0, max=300)])
    name_en = TextField(u'Название на англиском', validators=[Length(min=0, max=300)])
    troika_state = IntegerField(u'Статус в Тройке')
    status = StringField(u'Статус')

    def __init__(self, *args, **kwargs):
        super(CardForm, self).__init__(*args, **kwargs)

    def validate(self):
        initial_validation = super(CardForm, self).validate()
        if not initial_validation:
            return False

        try:
            self.id.data
        except:
            self.id.data = 0

        card = Card.query.filter(
            (Card.hard_id == self.hard_id.data) |
            (Card.troika_id == self.troika_id.data)).first()
        if card.id != self.id.data:
            self.hard_id.errors.append(u"Карта с таким набором параметров уже есть в базе")
            self.troika_id.errors.append(u"Карта с таким набором параметров уже есть в базе")
            return False
        return True
