import logging
from twisted.web.resource import Resource
from YubiReverseProxy import *


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
