from core.models.address import Address
from core.models.transaction import Transaction


class TxPool:
    def __init__(self):
        self.transactions: list[Transaction] = []

    def addTransaction(self,
                       sender: Address, receiver: Address, amount: float, fee: float, message: str) -> Transaction:
        tx = Transaction(sender, receiver, amount, fee, message)
        tx.sign(sender.keyPair)
        self.transactions.append(tx)
        return tx

    def getTransaction(self, signature) -> Transaction:
        for i in range(len(self.transactions)):
            if self.transactions[i].signature == signature:
                return self.transactions[i]
