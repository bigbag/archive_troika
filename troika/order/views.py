# -*- coding: utf-8 -*-
import logging

from flask import (Blueprint, abort, current_app, flash, render_template,
                   request)


logger = logging.getLogger(__name__)

blueprint = Blueprint("order", __name__, url_prefix='/order',
                      static_folder="../static")
