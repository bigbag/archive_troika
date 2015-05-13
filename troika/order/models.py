# -*- coding: utf-8 -*-
import logging

from troika.database import Model, SurrogatePK, db
from troika.helpers import date_helper

logger = logging.getLogger(__name__)


class Order(SurrogatePK, Model):

    __tablename__ = 'orders'

    PER_PAGE = 50

    STATUS_NEW = 'new'
    STATUS_COMPLETED = 'completed'
    STATUS_ERROR = 'error'

    user_id = db.Column(db.Integer(), nullable=False, unique=True)
    user_email = db.Column(db.String(128), nullable=False, unique=True)
    image = db.Column(db.String(512), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)
    update_date = db.Column(db.DateTime, default=date_helper.get_current_date())
    status = db.Column(db.String(128), nullable=False, default=STATUS_NEW)

    def save(self):
        self.update_date = date_helper.get_current_date()
        if not self.status:
            self.status = self.STATUS_NEW

        if not self.creation_date:
            self.creation_date = date_helper.get_current_date()

        return super(Order, self).save()
