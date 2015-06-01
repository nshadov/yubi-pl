#!/usr/bin/env python

import logging
from twisted.internet import reactor
# ---
from YubiProxy import YubiProxy
# --- ---

logging.basicConfig(filename="debug.log", level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(module)sf:%(funcName)s: %(message)s")




def main():
    logging.info("=======================[ STARTING ... ]=======================")

    yp = YubiProxy("blog.whitecatsec.com", 80)
    reactor.listenTCP(8080, yp.getSite())
    reactor.run()

    logging.info("=======================[ FINISHED ]=======================")


if __name__ == "__main__":
    try:
        main()
    except Exception, e:
        logging.error("Last resort exception handler. Exception caught! %s" % e)
        print e
        sys.exit(-1)

