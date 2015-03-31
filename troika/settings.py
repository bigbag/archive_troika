# -*- coding: utf-8 -*-
import os

from troika.helpers.logging_helper import setup_loggers

os_env = os.environ


class Config(object):
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    APP_HOST = '0.0.0.0'
    APP_PORT = 7777

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # COOKIE
    COOKIE_NAME = "troika_mobispot"
    COOKIE_HTTPONLY = True
    COOKIE_SECURE = "strong"
    SESSION_PROTECTION = "strong"

    # MAIL
    MAIL_DEFAULT_SENDER = ""
    MAIL_SERVER = '127.0.0.1'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None

    # TIMEZONES
    TIME_ZONE = 'Europe/Moscow'

    # CSRF & SECRET_KEY
    BCRYPT_LOG_ROUNDS = 13

    SECRET_KEY = 'SECRET_KEY_FOR_SESSION_SIGNING'

    CSRF_ENABLED = True
    CSRF_SESSION_KEY = 'SOMETHING_IMPOSSIBLE_TO_GUEES'
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True

    WTF_CSRF_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']

    TESTING = False

    # DEBUG
    DEBUG = False
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # TIMEZONES
    TIME_ZONE = 'UTC'

    # DATABASES
    SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/troika?charset=utf8'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_RECORD_QUERIES = True

    # CACHE
    CACHE_TYPE = 'simple'
    CACHE_KEY_PREFIX = 'transpot_'
    CACHE_DEFAULT_TIMEOUT = 50
    CACHE_THRESHOLD = 2048

    # TEMP
    TEMP_DIR = os.path.join(PROJECT_ROOT, 'tmp')

    # BABEl
    BABEL_DEFAULT_LOCALE = 'ru'
    BABEL_DEFAULT_FOLDER = 'translations'
    LANGUAGES = {
        'en': {'flag': 'gb', 'name': 'English'},
        'ru': {'flag': 'ru', 'name': 'Russian'}
    }

    # LOGGING
    LOG_ENABLE = True
    LOG_LEVEL = 'ERROR'
    LOG_MAX_SIZE = 1024 * 1024
    LOG_DIR = os.path.join(PROJECT_ROOT, 'logs')
    LOG_SETTINGS = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(levelname)s] [P:%(process)d] [%(asctime)s] %(pathname)s:%(lineno)d: %(message)s',
                'datefmt': '%d/%b/%Y %H:%M:%S',
            },
            'simple': {
                'format': '[%(levelname)s] [P:%(process)d] [%(asctime)s] %(message)s',
                'datefmt': '%d/%b/%Y %H:%M:%S',
            },
        }
    }

    # BUSINESS
    ISSUERS = 111

    FTP_HOST = ''
    FTP_USER = ''
    FTP_PASSWORD = ''

    setup_loggers(LOG_SETTINGS, LOG_ENABLE, LOG_LEVEL, LOG_DIR, LOG_MAX_SIZE)


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
