#!/usr/bin/env python

# Run this with
# PYTHONPATH=. DJANGO_SETTINGS_MODULE=neatapps.settings tornado_main.py

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "clavutich.settings")

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

define('port', type=int, default=5555)


def main():
    parse_command_line()
    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
        [('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)), ], debug=True, autoreload=True)
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
