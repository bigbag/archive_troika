# -*- coding: utf-8 -*-
import gzip
import StringIO
from functools import wraps

from flask import make_response


def add_response_headers(headers={}):
    """This decorator adds the headers passed in to the response"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator


def csv_headers(f):
    @wraps(f)
    @add_response_headers({'Content-Type': 'text/csv'})
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function


def xml_headers(f):
    @wraps(f)
    @add_response_headers({'Content-Type': 'application/xml; charset=windows-1251'})
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function


def json_headers(f):
    @wraps(f)
    @add_response_headers({'Content-Type': 'application/json'})
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function


def gzip_content(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        resp = make_response(f(*args, **kwargs))

        gzip_buffer = StringIO.StringIO()
        gzip_file = gzip.GzipFile(
            mode='wb',
            compresslevel=6,
            fileobj=gzip_buffer)
        gzip_file.write(resp.data)
        gzip_file.close()
        resp.data = gzip_buffer.getvalue()

        h = resp.headers
        h['Content-Type'] = 'application/gzip'
        h['Content-Encoding'] = 'gzip'
        h['Content-Length'] = len(resp.data)

        return resp
    return decorated_function
