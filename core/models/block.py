from ..helpers.helpers import calculateDifficulty, serializeSHA256, littleEndian
import json
from ..consts import BLOCK_REWARD, MAX_BLOCK_SIZE
import sys


class Block:
    def __init__(self, timestamp, version, previous_hash, merkle_root, difficulty, nonce, transactions, height=1):
        self.version = version
        self.previous_hash = previous_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.difficulty = difficulty
        self.nonce = nonce
        self.transactions = transactions
        self.hash = self.getHash()
        self.height = height

    def __str__(self) -> str:
        return '''
            Height: {}
            Version: {}
            Previous hash: {}
            Merkle root: {}
            Timestamp: {}
            Difficulty: {}
            Nonce: {}
            Timestamp: {}
            Hash: {}
            Transactions: {}
            '''.format(self.height, self.version, self.previous_hash, self.merkle_root, self.timestamp, self.difficulty,
                       self.nonce, self.timestamp, self.hash, self.transactions)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def verify(self):
        return int(
            self.hash, 16) < calculateDifficulty(self.difficulty) and sys.getsizeof(
            self.transactions) <= MAX_BLOCK_SIZE and self.transactions[0].amount == BLOCK_REWARD

    def getHash(self):
        return littleEndian(serializeSHA256(serializeSHA256(
            self.version + littleEndian(self.previous_hash) + littleEndian(self.merkle_root) +
            littleEndian(hex(self.timestamp)) + littleEndian(hex(self.difficulty)) + littleEndian(hex(self.nonce)))))
