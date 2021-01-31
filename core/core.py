from .helpers.helpers import generateMerkleRoot
from .models.transaction import Transaction
from .txpool import TxPool
from .models.block import Block
from .helpers.linkedlist import LinkedList
from .consts import CHAIN_VERSION, TARGET_DIFF


class Core:
    def __init__(self):
        self.chain = LinkedList()
        self.transaction_pool: TxPool = TxPool()

    def addBlock(self, transactions: list[Transaction], nonce):
        block: Block
        lastBlock = self.chain.getLast()
        if lastBlock is None:
            block = Block(CHAIN_VERSION, '', generateMerkleRoot(transactions), TARGET_DIFF, nonce, transactions)
        else:
            block = Block(
                CHAIN_VERSION, lastBlock.value.getHash(),
                generateMerkleRoot(transactions),
                TARGET_DIFF, nonce, transactions)
        if block.verify():
            self.consumeBlockTransactions(block)
            self.chain.addNode(block)
            return block
        else:
            return None

    def addTransaction(self, sender: str, receiver: str, amount: float, fee: float, signature: str, pubkey: str,
                       message: str) -> Transaction:
        return self.transaction_pool.addTransaction(sender, receiver, amount, fee, signature, pubkey, message)

    def consumeBlockTransactions(self, block: Block):
        idx = 0
        while idx < len(block.transactions):
            tx = block.transactions[idx]
            self.transaction_pool.consumeTransaction(tx)
            idx += 1

    def printChain(self):
        self.chain.printList()

    def toList(self):
        return self.chain.toList()
