# -*- coding: utf-8 -*-

from troika.database import Model, SurrogatePK, db
from troika.helpers import date_helper


class Report(SurrogatePK, Model):

    __tablename__ = 'reports'

    PER_PAGE = 50

    STATUS_NEW = 'new'
    STATUS_INPROGRESS = 'inprogress'
    STATUS_SENT = 'sent'
    STATUS_ERROR = 'error'

    name = db.Column(db.String(300))
    creation_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(128), nullable=False, default=STATUS_NEW)

    def __init__(self, name=None, **kwargs):
        if name:
            self.name = name
            self.creation_date = date_helper.get_current_date()
            self.status = self.STATUS_NEW

        db.Model.__init__(self, **kwargs)

    def __repr__(self):
        return '<Report ({name!r})>'.format(name=self.name)
