from .helpers.linkedlist import LinkedList

MAX_NONCE = 1000000000
TARGET_DIFF = 0x0000ffff00000000000000000000000000000000000000000000000000000000
CHAIN_VERSION = '01000000'


class Core:
    def __init__(self):
        self.chain = LinkedList()
        pass

    def addBlock(self, block):
        self.chain.addNode(block)

    def printChain(self):
        self.chain.printList()
