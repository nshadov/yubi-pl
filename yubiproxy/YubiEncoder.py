import logging
from bs4 import BeautifulSoup, Comment
from Crypto.Hash import SHA256


class YubiEncoder:
    def __init__(self):
        logging.debug("Creating new Encoder")

    def modifyRequest(self, method, path, request):
        request.requestHeaders.setRawHeaders(b"accept-encoding", [b"identity"])

    def modifyResponseBuffer(self, buffer):
        page = BeautifulSoup(buffer)
        
        # PUT YOUR RESPONSE PAGE MODIFICATIONS HERE

        # CREATE HASH SHA-256 SIGNATURE
        page = self.createSignature(page)

        return page.prettify().encode("utf-8")

    def createSignature(self, page):
        hash = SHA256.new(page.prettify().encode("ascii")).hexdigest()
        logging.debug("Adding SHA-256 Hash: %s" % hash)

        body = page.body
        comment = u"SHA-256 Hash: %s" % hash
        comment_tag = page.new_string(comment, Comment)
        body.append(comment_tag)

        return page
