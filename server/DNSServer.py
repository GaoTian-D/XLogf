#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
- file name: DNSServer.py
- date: 29/01/2023
"""
from settings.ConfigLoad import main_config
from database.RedisHelper import RedisHelper
from common.func import get_current_time, get_second_timestamp
from twisted.internet import defer, reactor
from twisted.names import dns, error, server
from common.logger import logger

'''
https://docs.twisted.org/en/stable/names/howto/custom-server.html
'''


def _patch_handleQuery(self, message, protocol, address):
    query = message.queries[0]
    return (
        self.resolver.query(query, address)
            .addCallback(self.gotResolverResponse, protocol, message, address)
            .addErrback(self.gotResolverError, protocol, message, address)
    )


'''
增加源地址信息 IP:Port
'''
server.DNSServerFactory.handleQuery = _patch_handleQuery


class DynamicResolver:
    """
    定制的 DNS 解析器
    """
    _support_types = []
    _typesMap = {
        'AAAA': 28, 'A': 1, 'CNAME': 5, 'MX': 15, 'NS': 2
    }

    def __init__(self):
        self._suffixes = main_config.dnslog['suffixes']
        self._allows = {'persistent': [], 'temporary': []}
        self._update_interval = main_config.dnslog['update_interval']
        self._redisHelper = RedisHelper(host=main_config.redis['host'], port=main_config.redis['port'])
        # 立即载入 redis 当前配置
        self._last_second_timestamp = 0
        for k, v in self._typesMap.items():
            if k in main_config.dnslog['support_types']:
                self._support_types.append(v)

    def _dynamicResponseRequired(self, query, address):
        """
        只响应 A 和 AAAA, 分别对应 1 和 28
        """
        if query.cls == 1 and query.type in self._support_types:
            ask = str(query.name)
            # labels = ask.split(".")
            # print(labels)
            ''' 是否命中 '''
            for suffix in self._suffixes:
                if ask.endswith(suffix):
                    '''加载域名配置信息'''
                    current_second_timestamp = get_second_timestamp()
                    if current_second_timestamp - self._last_second_timestamp > self._update_interval:
                        # 定时更新配置
                        keylist = self._redisHelper.keys('xlogf:domain:persistent:*')
                        for key in keylist:
                            v = key.decode("utf-8")[len('xlogf:domain:persistent:'):]
                            self._allows['persistent'].append(v)

                        keylist = self._redisHelper.keys('xlogf:domain:temporary:*')
                        for key in keylist:
                            v = key.decode("utf-8")[len('xlogf:domain:temporary:'):]
                            self._allows['temporary'].append(v)
                        self._last_second_timestamp = current_second_timestamp


                    for prefix in self._allows['persistent']:
                        allow = '{p}.{s}'.format(p=prefix, s=suffix)
                        if ask.endswith(allow):
                            # c = dns.QUERY_CLASSES.get(query.cls, "UNKNOWN (%d)" % query.cls)
                            t = dns.QUERY_TYPES.get(
                                query.type, dns.EXT_QUERIES.get(query.type, "UNKNOWN (%d)" % query.type)
                            )
                            addr = '%s:%s' % (address[0], address[1])
                            line = '%s, %s, %s, %s' % (query.name, t, addr, get_current_time())
                            logger.info(line)
                            self._redisHelper.append_list_value('xlogf:domain:persistent:%s' % prefix, line)
                            return True

                    for prefix in self._allows['temporary']:
                        allow = '{p}.{s}'.format(p=prefix, s=suffix)
                        if ask.endswith(allow):
                            # c = dns.QUERY_CLASSES.get(query.cls, "UNKNOWN (%d)" % query.cls)
                            t = dns.QUERY_TYPES.get(
                                query.type, dns.EXT_QUERIES.get(query.type, "UNKNOWN (%d)" % query.type)
                            )
                            addr = '%s:%s' % (address[0], address[1])
                            line = '%s, %s, %s, %s' % (query.name, t, addr, get_current_time())
                            logger.info(line)
                            self._redisHelper.append_list_value('xlogf:domain:temporary:%s' % prefix, line)
                            return True
        return False

    def _doDynamicResponse(self, query, answer_ip):
        """
        封装响应
        """
        name = str(query.name)
        # labels = ask.split(".")
        # parts = labels[0].split(self._pattern)
        # lastOctet = int(parts[1])
        answer = dns.RRHeader(
            name=name,
            payload=dns.Record_A(address='%s' % (answer_ip)),
        )
        answers = [answer]
        authority = []
        additional = []
        return answers, authority, additional

    def query(self, query, address):
        """
        域名解析核心函数
        """
        ask = str(query.name)
        # 管理域名 不需要了 coredns 解决
        # if ask in main_config.dnslog['manage']:
        #     host = main_config.dnslog['host']
        #     return defer.succeed(self._doDynamicResponse(query, host))
        # 保留域名
        # if ask in main_config.dnslog['reserve']:
        #     value = main_config.dnslog['mapping'].get(ask)
        #     if value:
        #         return defer.succeed(self._doDynamicResponse(query, value))
        #     return defer.fail(error.DomainError())
        # DNSLOG 的功能
        if self._dynamicResponseRequired(query, address):
            return defer.succeed(self._doDynamicResponse(query, '127.0.0.1'))
        else:
            return defer.fail(error.DomainError())


class XlogfDNS:
    def setUP(self, port=53):
        factory = server.DNSServerFactory(
            clients=[DynamicResolver()]
            # client.Resolver(resolv="/etc/resolv.conf")
        )
        protocol = dns.DNSDatagramProtocol(controller=factory)
        reactor.listenUDP(port, protocol)
        reactor.run()
