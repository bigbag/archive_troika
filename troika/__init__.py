# -*- coding: utf-8 -*-
import logging
from troika.app import create_app

from troika.card.models import Card
from troika.history.models import CardsHistory
from troika.order.models import Order
from troika.report.models import Report
from troika.user.models import User
from troika.campus.models import Campus

try:
    from troika.settings_local import Config
except Exception as e:
    logging.exception("Exception: %(body)s", {'body': e})
    from troika.settings import Config

app = create_app(Config)
