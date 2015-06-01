#!/usr/bin/env python

from twisted.internet import reactor

from YubiProxy import YubiProxy

yp = YubiProxy("blog.whitecatsec.com", 80)
reactor.listenTCP(8080, yp.getSite())
reactor.run()




