from time import time


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

    def sign(private_rsa, public_rsa):
        #  TODO: Verify data and sign with RSA private and public key!!!
        pass

    def verify():
        #  TODO: Sender must have amount + fee available in wallet!!!
        pass
