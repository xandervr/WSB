from json import JSONEncoder
from ..models.block import Block


class BlockEncoder(JSONEncoder):
    def default(self, z):
        if isinstance(z, Block):
            return {
                "version": z.version,
                "previous_hash": z.previous_hash,
                "merkle_root": z.merkle_root,
                "timestamp": z.timestamp,
                "difficulty": z.difficulty,
                "nonce": z.nonce,
                "hash": z.hash,
                "height": z.height,
                "transactions": list(map(lambda x: x.toJSON(), z.transactions))
            }
        else:
            return super().default(z)
