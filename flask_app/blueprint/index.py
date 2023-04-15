#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
- file name: index.py
- date: 30/01/2023
"""

from flask import (
    Blueprint
)
from flask import jsonify
bp = Blueprint('index', __name__, url_prefix='')


@bp.route('/', methods=['GET'])
def index():
    return '<html><body><h1>It works!</h1></body></html>'


@bp.route('/health', methods=['GET'])
def health():
    'Content-Type: application/vnd.spring-boot.actuator.v3+json'
    return jsonify(status="UP")
