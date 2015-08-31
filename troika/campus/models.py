# -*- coding: utf-8 -*-
import json

from flask.ext.login import current_user

from troika.database import Model, ReferenceCol, SurrogatePK, db, relationship
from troika.helpers import date_helper


class Campus(SurrogatePK, Model):

    __tablename__ = 'campus'

    PER_PAGE = 50

    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    zip = db.Column(db.String(16))
