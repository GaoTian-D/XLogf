#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
- file name: HTTPServer.py
- date: 30/01/2023
"""

from twisted.web import server
from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints
from twisted.web.pages import notFound
from twisted.web.static import File


class LogPage(Resource):
    # 是否页节点
    isLeaf = True

    def __init__(self):
        Resource.__init__(self)
        # self.year = year

    def render_GET(self, request):
        print(request.args)
        # 当前路径 request.prepath, 剩余路径列表 request.postpath
        return "Hello, world! I am located at %r %r.".encode('utf-8') % (request.prepath, request.postpath)


class GetdomainPage(Resource):
    '''
    添加一个永久域名
    '''
    isLeaf = True
    _args_key_1 = b'name'

    def __init__(self):
        Resource.__init__(self)
        # self.year = year
    def render_GET(self, request):
        request.setHeader('Content-Type', 'text/html; charset=UTF-8')
        if request.args.get(self._args_key_1) and len(request.args[self._args_key_1]) == 1:
            return "Add 永久域名 %s".encode('utf-8') % request.args[self._args_key_1][0]
        return '<html><body><h1>It works!</h1></body></html>'.encode('utf-8')


class CustomSite(server.Site):
    def getResourceFor(self, request):
        request.setHeader('server', 'nginx/1.20.1')
        return server.Site.getResourceFor(self, request)


class MyHttpHandler(Resource):

    def render_GET(self, request):
        request.setHeader('Content-Type', 'text/html; charset=UTF-8')
        return '<html><body><h1>It works!</h1></body></html>'.encode('utf-8')

    def getChild(self, name, request):
        print(name, request)
        if name == b'':
            return self
        if name == b'getdomain.php':
            return GetdomainPage()
        return LogPage()


root = MyHttpHandler()  # 通过 putChild 是静态方式
factory = CustomSite(root)

# 启动 TCP 监听
endpoint = endpoints.TCP4ServerEndpoint(reactor, 8090)
endpoint.listen(factory)
reactor.run()
