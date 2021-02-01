from .consts import TARGET_DIFF


class Params:
    def __init__(self, difficulty: int = TARGET_DIFF) -> None:
        self.difficulty = difficulty
