#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
- file name: config.py
- date: 30/01/2023
"""
from datetime import timedelta
import os

ROOT = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(ROOT, 'uploads')
ASSETS_FOLDER = os.path.join(ROOT, 'assets')
ENV = 'development'  # 'production'
# python3 -c 'import secrets; print(secrets.token_hex())'
SECRET_KEY = 'a1614544d576a328440d181c098'
# 上传大小限制 30 M
MAX_CONTENT_LENGTH = 30 * 1000 * 1000
# 会话
SESSION_COOKIE_NAME = "JSESSIONID"
# PERMANENT_SESSION_LIFETIME = timedelta(hours=4)
# 总是返回一个 session
SESSION_REFRESH_EACH_REQUEST = True
PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

REDIS_HOST = os.environ.get('REDIS_HOST', "127.0.0.1")
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

REDIS_URL = "redis://{}:{}/0".format(REDIS_HOST, REDIS_PORT)
print("==>" + REDIS_URL)
DOMAIN_SUPPFIX = os.environ.get('LISTEN_DOMAIN', "sup0rnm4n.com")
print("==>" + DOMAIN_SUPPFIX)
# 临时域名 30 分钟有效期
DOMAIN_EXPIRE = 1800
