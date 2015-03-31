# -*- coding: utf-8 -*-
import calendar
import time
from datetime import datetime

import pytz
from pytz import timezone


def get_current_date(format='%Y-%m-%d %H:%M:%S'):
    client_time = datetime.utcnow()
    if format:
        client_time = client_time.strftime(format)
    return client_time


def get_current_utc():
    return calendar.timegm(datetime.utcnow().utctimetuple())


def to_utc(date, tz):
    tz = timezone(tz)
    utc = pytz.timezone('UTC')
    d_tz = tz.normalize(tz.localize(date))
    d_utc = d_tz.astimezone(utc).replace(tzinfo=None)
    return d_utc


def from_utc(date, tz):
    tz = timezone(tz)
    utc = pytz.timezone('UTC')
    d_tz = utc.normalize(utc.localize(date))
    localetime = d_tz.astimezone(tz)
    return localetime


def convert_date_to_utc(date, tz, input, output):
    conv = datetime.strptime(date, input)
    return to_utc(conv, tz).strftime(output)


def convert_date_from_utc(date, tz, input, output):
    conv = datetime.strptime(date, input)
    return from_utc(conv, tz).strftime(output)


def get_timezone(tzname):
    now = datetime.utcnow()
    tz = pytz.timezone(tzname)
    utc = pytz.timezone('UTC')
    utc.localize(datetime.now())

    if utc.localize(now) > tz.localize(now):
        delta = str(utc.localize(now) - tz.localize(now))
        sign = '-'
    else:
        delta = str(tz.localize(now) - utc.localize(now))
        sign = '+'

    if len(delta) < 8:
        delta = "0%s" % delta
    return "%s%s%s" % (tz.tzname(now, is_dst=False), sign, delta)


def validate_date(d, format):
    try:
        time.strptime(d, format)
        return True
    except ValueError:
        return False
