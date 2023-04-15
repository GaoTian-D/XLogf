#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
- file name: func.py
- date: 30/01/2023
"""

import string, time
import random, base64
from datetime import datetime, date


def random_generator(size=10, chars=string.ascii_letters + string.digits + '!@%'):
    return ''.join(random.choice(chars) for _ in range(size))


def random_prefix_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def write_to_file(file, data):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(data + '\n')


def current_timestamp_millisecond():
    now = time.time()
    return int(round(now * 1000))


def current_timestamp_second():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return int(timestamp)


# def utc2cst(utc):
#     from_zone = tz.gettz('UTC')
#     to_zone = tz.gettz('Asia/Shanghai')
#     utc = datetime.datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ")
#     utc = utc.replace(tzinfo=from_zone)
#     cst = utc.astimezone(to_zone)
#     return cst
def timestame_convert(timestamp: int):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


def today():
    today = date.today()
    return today.strftime("%Y-%m-%d")


def custom_base64_decode(base64Str):
    s1 = "WZYXABCDEFGHIJKLMNOPQRSTUVzyxabcdefghijklmnopqrstuvw0123456789+/"
    s2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    return base64.b64decode(base64Str.translate(str.maketrans(s1, s2))).decode()
