#!/usr/bin/env python

import sys
import logging
from twisted.internet import reactor
from twisted.web.server import Site
# ---
from YubiProxy import YubiProxy
# --- ---

logging.basicConfig(filename="debug.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(module)sf:%(funcName)s: %(message)s")




def main():
    logging.info("=======================[ STARTING ... ]=======================")

    yp = YubiProxy("blog.whitecatsec.com", 80)

    reactor.listenTCP(8080, Site(yp))
    reactor.run()

    logging.info("=======================[ FINISHED ]=======================")


if __name__ == "__main__":
    try:
        main()
    except Exception, e:
        logging.error("Last resort exception handler. Exception caught! %s" % e)
        logging.exception("EXCEPTION")
        raise

