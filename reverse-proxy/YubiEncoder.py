import logging

class YubiEncoder:
    def __init__(self):
        pass

    def modify_request(self, method, path, request):
        request.requestHeaders.setRawHeaders(b"accept-encoding", [b"identity"])

    def modify_response_buffer(self, buffer):
        return buffer.upper()

