#!/usr/bin/env python
#
#
#

RHOST = "blog.whitecatsec.com"
RPORT = 80

LPORT = 8080

from twisted.internet import reactor
from twisted.web import proxy, server

site = server.Site(proxy.ReverseProxyResource(RHOST, RPORT, ''))
reactor.listenTCP(LPORT, site)
reactor.run()
