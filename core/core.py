from .models.transaction import Transaction
from .txpool import TxPool
from .models.address import Address
from .models.block import Block
from .helpers.linkedlist import LinkedList

MAX_NONCE = 1000000000
TARGET_DIFF = 0x0000ffff00000000000000000000000000000000000000000000000000000000
CHAIN_VERSION = '01000000'


class Core:
    def __init__(self):
        self.chain = LinkedList()
        self.transaction_pool: TxPool = TxPool()

    def addBlock(self, block: Block):
        self.chain.addNode(block)

    def addTransaction(self,
                       sender: Address, receiver: Address, amount: float, fee: float, message: str) -> Transaction:
        return self.transaction_pool.addTransaction(sender, receiver, amount, fee, message)

    def generateWallet(self):
        return Address()

    def printChain(self):
        self.chain.printList()
