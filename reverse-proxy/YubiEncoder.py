from twisted.web import iweb
from time import sleep

from zope.interface import implementer

@implementer(iweb._IRequestEncoderFactory)
class YubiEncoderFactory(object):
    def encoderForRequest(self, request):
        logging.debug("Requested new encoder from factory.")
        cookies = request.requestHeaders.getRawHeaders('cookie', [])
        key = "AAAA"
        return YubiEncoder(key, request)

@implementer(iweb._IRequestEncoder)
class YubiEncoder(object):
    def __init__(self, key, request):
        logging.debug("Init encoding request: %s" % request )
        self._key = key
        self._request = request

    def encode(self, data):
        logging.debug("Encoding part of request: %s" % request)
        return data.upper()

    def finish(self):
        logging.debug("Finished.")
        return None
