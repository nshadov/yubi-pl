import logging
from bs4 import BeautifulSoup

class YubiEncoder:
    def __init__(self):
        logging.debug("Creating new Encoder")

    def modify_request(self, method, path, request):
        request.requestHeaders.setRawHeaders(b"accept-encoding", [b"identity"])

    def modify_response_buffer(self, buffer):
        page = BeautifulSoup(buffer)

        # PUT YOUR RESPONSE PAGE MODIFICATIONS HERE

        return page.prettify().encode("ascii")

