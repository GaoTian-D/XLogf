#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
- file name: func.py
- date: 30/01/2023
"""
from datetime import datetime

def get_current_time():
    current = datetime.now()
    return current.strftime("%Y-%m-%d %H:%M:%S")

def get_second_timestamp():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return int(timestamp)

