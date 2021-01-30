from time import time
from ..helpers import rsa


class Transaction:
    def __init__(self, sender, receiver, amount, fee, message=""):
        self.timestamp = int(time())
        self.timestamp = 0
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee
        self.message = message
        self.signature = ''

    def sign(self, keyPair):
        data = f"{self.timestamp}{self.sender}{self.receiver}{self.amount}{self.fee}{self.message}"
        return rsa.generateSignature(data, keyPair)

    def verify(self, signature, keyPair):
        data = f"{self.timestamp}{self.sender}{self.receiver}{self.amount}{self.fee}{self.message}"
        return rsa.verifyKeyPairAndSignature(data, signature, keyPair)
