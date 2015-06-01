import urlparse
from urllib import quote as urlquote

from twisted.internet import reactor
from twisted.web import proxy, server, resource
from twisted.web.server import NOT_DONE_YET

class YubiReverseProxyClient(proxy.ProxyClient):
    def handleHeader(self, key, value):
        proxy.ProxyClient.handleHeader(self, key, value)

class YubiReverseProxyClientFactory(proxy.ProxyClientFactory):
    protocol = YubiReverseProxyClient

class YubiReverseProxy(proxy.Resource):
    proxyClientFactoryClass = YubiReverseProxyClientFactory

    def __init__(self, rhost, rport, path, reactor=reactor):
        proxy.Resource.__init__(self)
        self._rhost = rhost
        self._rport = rport
        self._path = path
        self._reactor = reactor


    def getChild(self, path, request):
        """
        Create and return a proxy resource with the same proxy configuration
        as this one, except that its path also contains the segment given by
        C{path} at the end.
        """
        return YubiReverseProxy(
            self._rhost, self._rport, self._path + '/' + urlquote(path, safe=""),
            self._reactor)
    
    def render(self, request):
        """
        Render a request by forwarding it to the proxied server.
        """
        # RFC 2616 tells us that we can omit the port if it's the default port,
        # but we have to provide it otherwise
        if self._rport == 80:
            host = self._rhost
        else:
            host = "%s:%d" % (self._rhost, self._rport)
        request.requestHeaders.setRawHeaders(b"host", [host])
        request.content.seek(0, 0)
        qs = urlparse.urlparse(request.uri)[4]
        if qs:
            rest = self._path + '?' + qs
        else:
            rest = self._path
        clientFactory = self.proxyClientFactoryClass(
            request.method, rest, request.clientproto,
            request.getAllHeaders(), request.content.read(), request)
        self._reactor.connectTCP(self._rhost, self._rport, clientFactory)
        return NOT_DONE_YET
