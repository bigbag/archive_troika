# -*- coding: utf-8 -*-
import logging

from troika.database import Model, SurrogatePK, db
from troika.helpers import date_helper

logger = logging.getLogger(__name__)


class Order(SurrogatePK, Model):

    __tablename__ = 'orders'

    PER_PAGE = 50

    STATUS_NEW = 'new'
    STATUS_REGISTERED = 'registred'
    STATUS_ERROR = 'error'

    mobispot_user_id = db.Column(db.Integer(), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(128), nullable=False, default=STATUS_NEW)

    def __init__(self, mobispot_user_id=None, **kwargs):
        if mobispot_user_id:
            self.mobispot_user_id = mobispot_user_id
            self.creation_date = date_helper.get_current_date()
            self.status = self.STATUS_NEW

        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return '<Order for user ({mobispot_user_id!r})>'.format(name=self.mobispot_user_id)
