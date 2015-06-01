from twisted.web.server import Site
from twisted.web import proxy
from twisted.web.resource import Resource, EncodingResourceWrapper

from YubiEncoder import YubiEncoderFactory
from YubiReverseProxy import YubiReverseProxy


class Static(Resource):
    isLeaf = True
    def render_GET(self, request):
        return "<html>Hello, world!</html>"

class YubiProxy:
    def __init__(self, dhost, dport):
        self._dhost = dhost
        self._dport = dport
        self._path = ""
        
    def _getProxy(self):
        #resource = Simple()
        #resource = proxy.ReverseProxyResource(self._dhost, self._dport, self._path)
        resource = YubiReverseProxy(self._dhost, self._dport, self._path)
        return self._getWrapper(resource)

    def _getWrapper(self, resource):
        return EncodingResourceWrapper(resource, [YubiEncoderFactory()])        

    def getSite(self):
        site = self._getProxy()
        self._site = Site(site)
        return self._site

