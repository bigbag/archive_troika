# -*- coding: utf-8 -*-
from flask.ext.assets import Bundle, Environment

css = Bundle(
    "libs/bootstrap/dist/css/bootstrap.css",
    "css/bootstrap-cerulean.min.css",
    "css/style.css",
    filters="cssmin",
    output="public/css/common.css"
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/angular/dist/angular.js",
    "libs/bootstrap/dist/js/bootstrap.js",
    "js/script.js",
    "angular/app.js",
    "angular/controllers/card.js",
    filters='jsmin',
    output="public/js/common.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", css)
