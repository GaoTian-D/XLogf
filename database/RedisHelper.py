#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
- file name: RedisHelper.py
- date: 30/01/2023
"""
import redis


class RedisHelper(object):
    def __init__(self, host, port):
        pool = redis.ConnectionPool(host=host, port=port)
        self.db = redis.Redis(connection_pool=pool)
        self.pipe = self.db.pipeline()

    def exists(self, name):
        return self.db.exists(name)

    def keys(self, pattern):
        return self.db.keys(pattern)

    def append_list_value(self, name, value):
        return self.db.rpush(name, value)

    def get_sets_value(self, name) -> set:
        value = self.db.smembers(name)
        if not value:
            return {}
        assert isinstance(value, set)
        return value

    def get_str_value(self, name):
        value = self.db.get(name)
        if not value:
            return None
        assert isinstance(value, bytes)
        return value.decode("utf-8")

    def set_str_value(self, name, value, expire=None):
        self.pipe.delete(name)
        self.pipe.set(name, value, expire)
        self.pipe.execute()

    def delete(self, name):
        self.db.delete(name)

    def set_expire(self, name, seconds):
        self.db.expire(name, seconds)
