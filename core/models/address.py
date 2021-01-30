from hashlib import sha256
from ..helpers import rsa


class Address:
    def __init__(self):
        self.keyPair = rsa.generateKeyPair()

    def generateAddress(self):
        return hex(int.from_bytes(sha256(self.keyPair.publickey().exportKey()).digest(), byteorder='big'))
