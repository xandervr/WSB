from core.models.transaction import Transaction


class TxPool:
    def __init__(self):
        self.transactions: list[Transaction] = []

    def addTransaction(
            self, sender: str,
            receiver: str, amount: float, fee: float, signature, pubkey, message: str) -> Transaction:
        tx = Transaction(sender, receiver, amount, fee, signature, pubkey, message)
        if tx.verify(pubkey):
            self.transactions.append(tx)
            return tx
        else:
            return None

    def getTransaction(self, signature) -> Transaction:
        for i in range(len(self.transactions)):
            if self.transactions[i].signature == signature:
                return self.transactions[i]

    def consumeTransaction(self, tx: Transaction):
        if not tx.isCoinbaseTransaction:
            self.transactions.remove(tx)
