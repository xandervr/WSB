from .models.block import Block
from .consts import TARGET_DIFF


class Params:
    def __init__(self) -> None:
        self.difficulty = TARGET_DIFF
        self.last_difficulty_change_block: Block = None
