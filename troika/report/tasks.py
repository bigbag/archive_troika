# -*- coding: utf-8 -*-
from flask.ext.celery import single_instance

from troika.card.models import Card
from troika.database import db
from troika.extensions import celery
from troika.report.models import Report


@celery.task(bind=True)
@single_instance(lock_timeout=15 * 60)
def send_stop_list():
    cards = Card().get_locked()
    if not cards:
        return None

    file_name, day_id = Report.generate_name()
    if not Report.save_report_file(file_name, cards):
        return False

    report = Report(file_name)
    report.day_id = day_id
    report.save()

    result = Report.send_report_file(file_name)
    if not result:
        report.status = Report.STATUS_ERROR
        report.save()
        return False

    report.status = Report.STATUS_SENT
    report.save()

    for card in cards:
        card.report_id = report.id
        db.session.add(card)

    db.session.commit()
    return True
