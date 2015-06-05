import logging
from twisted.web import proxy
from twisted.web.resource import Resource, EncodingResourceWrapper
from twisted.web.server import Site

from YubiEncoder import YubiEncoderFactory
from YubiReverseProxy import *


class TestStatic(Resource):
    isLeaf = True
    def render_GET(self, request):
        return "<html>Hello, world!</html>"

class YubiProxy(Resource):
    isLeaf = False
    #isLeaf = True

    def __init__(self, dhost, dport):
        Resource.__init__(self)
        logging.debug("Creating new YubiProxy [RESOURCE]")
        self.dhost = dhost
        self.dport = dport
        self.path = "/"

        self.proxy = YubiReverseProxy(self.dhost, self.dport, self.path)
        self.putChild( "", self.proxy )

