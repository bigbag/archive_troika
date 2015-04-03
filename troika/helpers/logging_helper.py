# -*- coding: utf-8 -*-
"""Logging helper"""

import os


def setup_loggers(logs_settings, logs_enabled, logs_level, logs_dir,
                  logs_max_size):
    import logging
    import logging.config

    if not logs_enabled:
        return False

    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    logs_settings['handlers'] = {
        'console': {
            'level': logs_level,
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'all_file': {
            'level': logs_level,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'encoding': 'utf8',
            'maxBytes': logs_max_size,
            'backupCount': 20,
            'filename': "%s/all.log" % logs_dir
        },
        'celery_file': {
            'level': logs_level,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'encoding': 'utf8',
            'maxBytes': logs_max_size,
            'backupCount': 20,
            'filename': "%s/celery.log" % logs_dir
        },
        'gunicorn_file': {
            'level': logs_level,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            'encoding': 'utf8',
            'maxBytes': logs_max_size,
            'backupCount': 20,
            'filename': "%s/celery.log" % logs_dir
        }
    }

    logs_settings['loggers'] = {
        'troika': {
            'level': logs_level,
            'handlers': ['console', 'all_file']
        },
        'celery.worker': {
            'level': logs_level,
            'handlers': ['celery_file']
        },
        'gunicorn.error': {
            'level': logs_level,
            'handlers': ['console', 'gunicorn_file']
        },
        'gunicorn.access': {
            'level': logs_level,
            'handlers': ['console', 'gunicorn_file']
        },

    }
    logging.config.dictConfig(logs_settings)
