# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import IntegerField, StringField, TextField
from wtforms.validators import DataRequired, Length

from .models import Card


class CardForm(Form):

    id = IntegerField()
    hard_id = StringField('Hard ID', validators=[DataRequired(), Length(min=3, max=128)])
    troika_id = StringField('Troika ID', validators=[DataRequired(), Length(min=3, max=128)])
    name_ru = TextField('Russian name', validators=[Length(min=0, max=300)])
    name_en = TextField('English name', validators=[Length(min=0, max=300)])
    troika_state = IntegerField('Troika state')
    status = StringField('Status')

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

        card = Card.query.filter_by(hard_id=self.hard_id.data).first()
        if card.id != self.id.data:
            self.hard_id.errors.append("Card with the hard_id has already been added")
            return False

        card = Card.query.filter_by(troika_id=self.troika_id.data).first()
        if card.id != self.id.data:
            self.troika_id.errors.append("Card with the troika_id has already been added")
            return False
        return True
