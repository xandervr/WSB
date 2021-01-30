from time import time
from ..helpers import rsa
from .address import Address


class Transaction:
    def __init__(self, sender: Address, receiver: Address, amount: float, fee: float, message=""):
        self.timestamp = int(time())
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee
        self.message = message
        self.signature = ''

    def sign(self, keyPair):
        data = f"{self.timestamp}{self.sender}{self.receiver}{self.amount}{self.fee}{self.message}".encode('utf-8')
        self.signature = rsa.generateSignature(data, keyPair)

    def verify(self, keyPair):
        data = f"{self.timestamp}{self.sender}{self.receiver}{self.amount}{self.fee}{self.message}".encode('utf-8')
        return rsa.verifyKeyPairAndSignature(data, self.signature, keyPair)

    def __str__(self) -> str:
        return '''
                Timestamp: {}
                Sender: {}
                Receiver: {}
                Amount: {}
                Fee: {}
                Message: {}
                '''.format(self.timestamp, self.sender.generateAddress(),
                           self.receiver.generateAddress(), self.amount, self.fee, self.message)
