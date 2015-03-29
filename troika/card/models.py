# -*- coding: utf-8 -*-
import datetime as dt

from troika.database import (Column, Model, ReferenceCol, SurrogatePK, db,
                             relationship)


class Card(SurrogatePK, Model):

    __tablename__ = 'cards'

    STATUS_NEW = 'new'
    STATUS_INPROGRESS = 'inprogress'
    STATUS_RELEASED = 'released'
    STATUS_DELIVERED = 'delivered'
    STATUS_REMOVED = 'removed'

    STATUS_TITLE = {STATUS_NEW: u'Новая',
                    STATUS_INPROGRESS: u'В процессе',
                    STATUS_RELEASED: u'Выпущена',
                    STATUS_DELIVERED: u'Доставлена',
                    STATUS_REMOVED: u'Удалена'}

    STATE_ACTIVE = 0
    STATE_LOST = 1
    STATE_BROKEN = 3
    STATE_NOT_NEED = 5
    STATE_REISSUED = 6

    TROIKA_STATE_TITLE = {STATE_ACTIVE: u'Рабочая',
                          STATE_LOST: u'Утеряна',
                          STATE_BROKEN: u'Испорчена',
                          STATE_NOT_NEED: u'Не нужна',
                          STATE_REISSUED: u'Перевыпущена'}

    hard_id = db.Column(db.String(128), unique=True, nullable=False)
    troika_id = db.Column(db.String(128), unique=True, nullable=False)
    name_ru = db.Column(db.String(300))
    name_en = db.Column(db.String(300))
    creation_date = db.Column(db.DateTime, nullable=False)
    troika_state = db.Column(db.Integer(), nullable=False, default=STATUS_NEW)
    status = db.Column(db.String(128), nullable=False, default=STATE_ACTIVE)

    def __repr__(self):
        return '<Card ({hard_id!r})>'.format(hard_id=self.hard_id)


class CardsHistory(SurrogatePK, Model):

    __tablename__ = 'cards_history'

    card_id = ReferenceCol('cards', nullable=False)
    card = relationship('Card', backref='cards_history')
    user_id = ReferenceCol('users', nullable=False)
    user = relationship('User', backref='cards_history')
    before = db.Column(db.Text())
    after = db.Column(db.Text())
    action_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<History ({card_id!r})>'.format(card_id=self.card_id)
