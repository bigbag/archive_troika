# -*- coding: utf-8 -*-
import json

from flask import render_template

from troika.card.models import Card
from troika.database import Model, ReferenceCol, SurrogatePK, db, relationship
from troika.helpers import date_helper


class CardsHistory(SurrogatePK, Model):

    __tablename__ = 'cards_history'

    PER_PAGE = 50

    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'

    ACTION_TITLE = {ACTION_CREATE: u'Добавление',
                    ACTION_UPDATE: u'Изменение',
                    ACTION_DELETE: u'Удаление'}

    card_id = ReferenceCol('cards', nullable=False)
    card = relationship('Card', backref='cards_history')
    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='cards_history')
    action = db.Column(db.String(128), nullable=False)
    before = db.Column(db.Text())
    after = db.Column(db.Text())
    action_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, user_id=None, **kwargs):
        if user_id:
            self.user_id = user_id
            self.action_date = date_helper.get_current_date()

        db.Model.__init__(self, **kwargs)

    @staticmethod
    def to_text(data):
        card = json.loads(data) if data else None

        return render_template("history/history.txt",
                               card=card,
                               status_title=Card.STATUS_TITLE,
                               troika_state_title=Card.TROIKA_STATE_TITLE)

    def __repr__(self):
        return '<History ({card_id!r})>'.format(card_id=self.card_id)
