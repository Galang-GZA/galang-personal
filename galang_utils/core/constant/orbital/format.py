from typing import List


class DIG_Format:
    def __init__(self, side, guide_name: str, types: List):
        self.side = side
        self.guide_name = guide_name
        self.types = types

    @staticmethod
    def join_parts(*parts):
        return "_".join([p for p in parts if p]).strip("_")

    def name(self):
        return self.join_parts(self.side, self.guide_name, *self.types)
