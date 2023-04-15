#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
- file name: __init__.py
- date: 30/01/2023
"""

from http.server import BaseHTTPRequestHandler
from .patch import version_string, ModifyFlask
from flask_redis import FlaskRedis
from flask_app.tasks import *
from .extension import JwtCookieSessionInterface
import os

BaseHTTPRequestHandler.version_string = version_string

redis_client = FlaskRedis()

def create_app():
    '''
    Flask will automatically detect the factory (create_app or make_app) in myapp.
    '''
    app = ModifyFlask(__name__, instance_relative_config=True)
    app.session_interface = JwtCookieSessionInterface()
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), 'config.py'), silent=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    redis_client.init_app(app)

    scheduler.init_app(app)
    scheduler.start()

    from .blueprint import api
    app.register_blueprint(api.bp)

    from .blueprint import index
    app.register_blueprint(index.bp)


    return app
