# -*- coding: utf-8 -*-
from ftplib import FTP_TLS
from flask import current_app

from troika.extensions import celery


@celery.task()
def send_stop_list():
    ftps = FTP_TLS(current_app.config.get('FTP_HOST'))
    ftps.login(current_app.config.get('FTP_USER'),
               current_app.config.get('FTP_PASSWORD'))
    ftps.prot_p()

    demo = ftps.retrlines('LIST')

    # filename = 'remote_filename.bin'
    # print 'Opening local file ' + filename
    # myfile = open(filename, 'wb')

    # ftps.retrbinary('RETR %s' % filename, myfile.write)

    ftps.close()
    return demo
