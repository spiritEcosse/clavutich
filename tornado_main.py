#!/usr/bin/env python

# Run this with
# PYTHONPATH=. DJANGO_SETTINGS_MODULE=neatapps.settings tornado_main.py

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clavutich.settings")
from clavutich.settings_local import AUTORELOAD

# Activate your virtual env
activate_env = os.path.expanduser(os.path.join(BASE_DIR, ".env/bin/activate_this.py"))
execfile(activate_env, dict(__file__=activate_env))

from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
if django.VERSION[1] > 5:
    django.setup()
import logging

define('port', type=int, default=5555)


def main():
    parse_command_line()
    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
        [('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)), ], debug=True, autoreload=AUTORELOAD)
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    tornado.options.parse_command_line()
    logging.info('Starting up')
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
