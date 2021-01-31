from time import time
from ..helpers import rsa


class Transaction:
    def __init__(
            self, sender: str, receiver: str, amount: float, fee: float, signature: str, pubkey: str,
            message=""):
        self.timestamp = int(time())
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.fee = fee
        self.message = message
        self.signature = signature
        self.pubkey = pubkey
        self.isCoinbaseTransaction = sender == 'coinbase'

    # def sign(self, keyPair):
    #     data = f"{self.timestamp}{self.sender}{self.receiver}{self.amount}{self.fee}{self.message}".encode('utf-8')
    #     self.signature = rsa.generateSignature(data, keyPair)
    #     self.pubkey = keyPair.n

    def verify(self, pubkey):
        try:
            data = f"{self.sender}{self.receiver}{self.amount}{self.fee}{self.message}".encode('utf-8')
            return rsa.verifyKeyPairAndSignature(
                data, self.signature, pubkey) and self.sender == rsa.generateAddress(int(pubkey, 16))
        except Exception as e:
            print(e)

    def toJSON(self) -> str:
        return self.__dict__

    def __str__(self) -> str:
        return '''
                Timestamp: {}
                Sender: {}
                Receiver: {}
                Amount: {} WSB
                Fee: {} WSB
                Message: {}
                '''.format(self.timestamp, self.sender,
                           self.receiver, self.amount, self.fee, self.message)


def transactionFromJSON(o: dict) -> Transaction:
    tx = Transaction(o['sender'], o['receiver'], o['amount'], o['fee'], o['signature'], o['pubkey'], o['message'])
    tx.timestamp = o['timestamp']
    return tx
