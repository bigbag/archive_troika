# -*- coding: utf-8 -*-

import json
import logging
from troika.database import db
from troika.extensions import celery
from troika.order.models import Order
from troika.order.forms import OrderForm
from troika.utils import format_error


@celery.task()
def create_order_from_store(data):

    data_dict = json.loads(data)

    form = OrderForm(**data_dict)
    if form.validate():
        order = Order()
        form.populate_obj(order)
        if not order.save():
            return False
    else:
        logger = logging.getLogger(__name__)
        logger.debug('ORDER CREATE')
        logger.debug('Request data: %(data)s' % {'data': data})
        logger.debug('Form error: %(error)s' % {'error': format_error(form)})

    return True
