# -*- coding: utf-8 -*-
import csv
import os
import logging
from ftplib import FTP_TLS
from flask import current_app

from troika.database import Model, SurrogatePK, db
from troika.helpers import date_helper

logger = logging.getLogger(__name__)


class Report(SurrogatePK, Model):

    __tablename__ = 'reports'

    PER_PAGE = 50

    DEFAULT_DAY_ID = 1

    STATUS_NEW = 'new'
    STATUS_INPROGRESS = 'inprogress'
    STATUS_SENT = 'sent'
    STATUS_ERROR = 'error'

    name = db.Column(db.String(300))
    creation_date = db.Column(db.DateTime, nullable=False)
    day_id = db.Column(db.String(4), nullable=False)
    status = db.Column(db.String(128), nullable=False, default=STATUS_NEW)

    def __init__(self, name=None, **kwargs):
        if name:
            self.name = name
            self.creation_date = date_helper.get_current_date()
            self.status = self.STATUS_NEW

        db.Model.__init__(self, **kwargs)

    @staticmethod
    def generate_name():

        current_date = date_helper.get_current_date('%Y-%m-%d')
        last_report = Report.query.filter(Report.creation_date > current_date).\
            order_by('creation_date desc').limit(1).first()
        if not last_report:
            day_id = Report.DEFAULT_DAY_ID
        else:
            day_id = int(last_report.day_id) + 1
            if day_id > 99:
                day_id = Report.DEFAULT_DAY_ID

        name = "SL-%(issuer_id)s-%(date)s-%(day_id)02d.csv" % {
            'issuer_id': current_app.config.get('ISSUER_ID'),
            'date': date_helper.get_current_date('%y%m%d'),
            'day_id': day_id,
        }
        return name, "%02d" % day_id

    @staticmethod
    def get_report_file_path(file_name):

        return os.path.join(current_app.config.get('REPORT_DIR'), file_name)

    @staticmethod
    def save_report_file(file_name, cards):

        try:
            with open(Report.get_report_file_path(file_name), 'wb') as csvfile:
                writer = csv.writer(csvfile,
                                    delimiter=';',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
                for card in cards:
                    writer.writerow([card.troika_id, int(card.troika_state)])
        except Exception, e:
            logger.error('ERROR AT SAVE STOPLIST FILE')
            logger.error(e)
            return False
        else:
            return True

    @staticmethod
    def send_report_file(file_name):

        ftps = FTP_TLS(current_app.config.get('FTP_HOST'))
        ftps.login(current_app.config.get('FTP_USER'),
                   current_app.config.get('FTP_PASSWORD'))
        ftps.prot_p()

        result = ftps.storbinary('STOR /%(stoplist_dir)s/%(file_name)s' % {
            'stoplist_dir': current_app.config.get('FTP_STOPLIST_DIR'),
            'file_name': file_name},
            open(Report.get_report_file_path(file_name)))
        ftps.close()

        if '226' not in result:
            logger.error('ERROR AT SEND STOPLIST FILE')
            logger.error('File name: "%(file_name)s", result: "%(result)s"' % {
                'file_name': file_name,
                'result': result})
            return False

        logger.debug('SEND STOPLIST FILE')
        logger.debug('File name: "%(file_name)s", result: "%(result)s"' % {
            'file_name': file_name,
            'result': result})

        return True

    def __repr__(self):
        return '<Report ({name!r})>'.format(name=self.name)
