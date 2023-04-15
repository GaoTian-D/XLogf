#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
- file name: ConfigLoad.py
- date: 29/01/2023
"""
import yaml, codecs, os


class MainConfig:
    def __init__(self, yamlFile):
        with codecs.open(yamlFile, 'r', encoding='utf8') as stream:
            self._conf_yaml = yaml.load(stream, Loader=yaml.FullLoader)
        self.dnslog = {}
        # self.dnslog['suffixes'] = self._conf_yaml['dnslog']['suffixes']
        self.dnslog['suffixes'] = [os.environ.get('LISTEN_DOMAIN', "sup0rnm4n.com")]
        print('[+] 监听域名: %s' % self.dnslog['suffixes'])
        self.dnslog['support_types'] = self._conf_yaml['dnslog']['support_types']
        # self.dnslog['reserve'] = self._conf_yaml['dnslog']['reserve']
        # self.dnslog['host'] = self._conf_yaml['dnslog']['host']
        # self.dnslog['manage'] = self._conf_yaml['dnslog']['manage']
        # self.dnslog['mapping'] = {}
        # for mapping in self._conf_yaml['dnslog']['mapping']:
        #     if mapping.find(':'):
        #         k = mapping.split(':')[0]
        #         v = mapping.split(':')[1]
        #         self.dnslog['mapping'][k] = v
        self.dnslog['update_interval'] = int(self._conf_yaml['dnslog']['update_interval'])

        self.redis = {}
        self.redis['host'] = str(os.environ.get('REDIS_HOST', "127.0.0.1"))  # str(self._conf_yaml['redis']['host'])
        self.redis['port'] = int(os.environ.get('REDIS_PORT', 6379))  # int(self._conf_yaml['redis']['port'])


current_dir = os.path.dirname(os.path.realpath(__file__))
main_config = MainConfig(os.path.join(current_dir, "main.yaml"))
