#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
- file name: logger.py
- date: 30/01/2023
"""

import logging

# create logger
logger = logging.getLogger('XLogf')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)
