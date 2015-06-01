from twisted.web import iweb
from time import sleep

from zope.interface import implementer

@implementer(iweb._IRequestEncoderFactory)
class YubiEncoderFactory(object):
    def encoderForRequest(self, request):
        cookies = request.requestHeaders.getRawHeaders('cookie', [])
        key = "AAAA"
        return YubiEncoder(key, request)

@implementer(iweb._IRequestEncoder)
class YubiEncoder(object):
    def __init__(self, key, request):
        self._key = key
        self._request = request

    def encode(self, data):
        print "DATA:", data
        return data.upper()

    def finish(self):
        print "FINISH!"
        return None
