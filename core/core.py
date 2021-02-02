from .helpers.helpers import generateMerkleRoot
from .models.transaction import Transaction
from .txpool import TxPool
from .models.block import Block
from .helpers.linkedlist import LinkedList
from .consts import BLOCK_MINE_TIME_TARGET, CHAIN_VERSION, DIFFICULTY_BLOCKS, TARGET_DIFF_BITS, TARGET_DIFF_SHORT
import pickle
import time
from .params import Params


class Core:
    def __init__(self):
        self.chain = LinkedList()
        self.transaction_pool: TxPool = TxPool()
        self.params = Params()

    def saveChain(self):
        try:
            with open('chain', 'wb') as output:
                pickle.dump(self.chain, output, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(e)

    def loadChain(self):
        try:
            with open('chain', 'rb') as input:
                self.chain = pickle.load(input)
        except Exception as e:
            print(e)

    def saveParams(self):
        try:
            with open('params', 'wb') as output:
                pickle.dump(self.params, output, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(e)

    def loadParams(self):
        try:
            with open('params', 'rb') as input:
                self.params = pickle.load(input)
        except Exception as e:
            print(e)

    def saveTxPool(self):
        try:
            with open('txpool', 'wb') as output:
                pickle.dump(self.transaction_pool, output, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(e)

    def loadTxPool(self):
        try:
            with open('txpool', 'rb') as input:
                self.transaction_pool = pickle.load(input)
        except Exception as e:
            print(e)

    def getBlocksMinedSinceLastDay(self):
        durationToSearch = 60 * 60 * 24
        currTime = int(time.time())
        lastBlock = self.chain.getLast()
        cursor = lastBlock
        if lastBlock is None:
            return 0
        while cursor.prev is not None:
            if cursor.value.timestamp >= currTime - durationToSearch:
                cursor = cursor.prev
            else:
                break
        return lastBlock.value.height - cursor.value.height

    def calculateDifficultyAdjustment(self, expected, actual) -> float:
        if actual < 1:
            return 1.0
        return float(expected) / float(actual)

    def adjustDifficulty(self, currBlock: Block):
        genesisBlock = self.chain.head
        expectedTime = DIFFICULTY_BLOCKS * BLOCK_MINE_TIME_TARGET
        referenceBlock = self.params.last_difficulty_change_block
        if genesisBlock is None or currBlock is None:
            return
        if self.params.last_difficulty_change_block is None:
            referenceBlock = genesisBlock.value
        if (currBlock.height - referenceBlock.height >= DIFFICULTY_BLOCKS):
            self.params.last_difficulty_change_block = currBlock
            actualTime = currBlock.timestamp - referenceBlock.timestamp
            adj = self.calculateDifficultyAdjustment(expectedTime, actualTime)
            self.params.difficulty = int(self.params.difficulty * adj)
            if self.params.difficulty < TARGET_DIFF_BITS:
                self.params.difficulty = TARGET_DIFF_BITS

    def calculateHashrateToMine(self):
        return (self.params.difficulty * 2**32) / 600

    def calculateNetworkHashrate(self):
        genesisBlock = self.chain.head
        lastBlock = self.chain.getLast()
        if genesisBlock is not None and lastBlock is not None:
            todayBlocks = self.getBlocksMinedSinceLastDay()
            expectedBlocks = 24 * 60 * 60 / BLOCK_MINE_TIME_TARGET
            hash_rate = (todayBlocks/expectedBlocks) * self.calculateHashrateToMine()
            return hash_rate
        else:
            return 0

    def addBlock(self, transactions: list[Transaction], nonce, timestamp):
        block: Block
        lastBlock = self.chain.getLast()
        if lastBlock is None:
            block = Block(timestamp, CHAIN_VERSION, '', generateMerkleRoot(
                transactions), self.params.difficulty, nonce, transactions)
        else:
            block = Block(timestamp,
                          CHAIN_VERSION, lastBlock.value.getHash(),
                          generateMerkleRoot(transactions),
                          self.params.difficulty, nonce, transactions)
        if block.verify():
            self.consumeBlockTransactions(block)
            self.chain.addNode(block)
            self.adjustDifficulty(block)
            self.saveChain()
            self.saveParams()
            return block
        else:
            return None

    def addTransaction(self, sender: str, receiver: str, amount: float, fee: float, signature: str, pubkey: str,
                       message: str) -> Transaction:
        tx = self.transaction_pool.addTransaction(sender, receiver, amount, fee, signature, pubkey, message)
        self.saveTxPool()
        return tx

    def consumeBlockTransactions(self, block: Block):
        idx = 0
        while idx < len(block.transactions):
            tx = block.transactions[idx]
            self.transaction_pool.consumeTransaction(tx)
            idx += 1
        self.saveTxPool()

    def printChain(self):
        self.chain.printList()

    def toList(self):
        return self.chain.toList()
