import logging
import urlparse
from urllib import quote as urlquote

from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web import proxy, server, resource
from twisted.web.server import NOT_DONE_YET

class YubiReverseProxyClient(proxy.ProxyClient):
    def __init__(self, command, rest, version, headers, data, father):
        logging.debug("FATHER: %s" % father)
        proxy.ProxyClient.__init__(self, command, rest, version, headers, data, father)

    def handleHeader(self, key, value):
        logging.debug("Handeling header for new YRPC: %s = %s." % (key, value))
        proxy.ProxyClient.handleHeader(self, key, value)

    def handleResponsePart(self, buffer):
        logging.debug("Got Response Part: %d bytes." % len(buffer))
        self.father.write(buffer)

    def handleStatus(self, version, code, message):
        logging.debug("Got status: %s - %s" % (str(code), message))
        self.father.setResponseCode(int(code), message)

class YubiReverseProxyClientFactory(proxy.ProxyClientFactory):
    protocol = YubiReverseProxyClient

class YubiReverseProxy(proxy.ReverseProxyResource):
    proxyClientFactoryClass = YubiReverseProxyClientFactory

    def __init__(self, rhost, rport, path, reactor=reactor):
        logging.debug("Creating new PROXY (%s, %s, %s) [RESOURCE-PROXY]" % (rhost,rport,path))
        proxy.ReverseProxyResource.__init__(self, rhost, rport, path, reactor)

    def getChild(self, path, request):
        logging.debug("Getting child: %s (request: %s)" % (path, request))
        return YubiReverseProxy(
            self.host, self.port, self.path + '/' + urlquote(path, safe=""),
            self.reactor)

    def render(self, request):
        if self.port == 80:
            host = self.host
        else:
            host = "%s:%d" % (self.host, self.port)
        request.requestHeaders.setRawHeaders(b"host", [host])
        request.content.seek(0, 0)
        qs = urlparse.urlparse(request.uri)[4]
        if qs:
            rest = self.path + '?' + qs
        else:
            rest = self.path
        clientFactory = self.proxyClientFactoryClass(
            request.method, rest, request.clientproto,
            request.getAllHeaders(), request.content.read(), request)
        self.reactor.connectTCP(self.host, self.port, clientFactory)
        return NOT_DONE_YET
