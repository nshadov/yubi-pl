#!/usr/bin/env python
#
#
#

RHOST = "blog.whitecatsec.com"
RPORT = 80

LPORT = 8080

from twisted.internet import reactor
from twisted.web import proxy, server, resource

from twisted.web.resource import EncodingResourceWrapper

class YubiClient(proxy.ProxyClient):
    def handleHeader(self, key, value):
        ProxyClient.handleHeader(self, key, value)

class YubiClientFactory(proxy.ProxyClientFactory):
    protocol = YubiClient

class YubiProxy(proxy.ReverseProxyResource):
    proxyClientFactoryClass = YubiClientFactory

    def getChild(self, path, request):
        return self.__class__(RHOST, RPORT, "")

    def render(self, request):
        proxy.ReverseProxyResource.render(self, request)

yproxy = YubiProxy(RHOST, RPORT, '')

site = server.Site(yproxy)
reactor.listenTCP(LPORT, site)
reactor.run()
