#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
- file name: patch.py
- date: 30/01/2023
"""

from flask import (Flask, Response)

def version_string(self):
    """Return the server software version string."""
    return "openresty"


class ModifyFlask(Flask):
    def process_response(self, response: Response) -> Response:
        response.headers.pop('Allow', None)
        response.headers['X-Application-Context'] = "prod-web-server:8181"
        return super().process_response(response)
