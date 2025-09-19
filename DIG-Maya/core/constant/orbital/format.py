from typing import List


class Global_Format:
    def __init__(self, side, base_name: str, labels: List):
        self.side = side
        self.base_name = base_name
        self.labels = labels

    @staticmethod
    def join_parts(*parts):
        return "_".join([p for p in parts if p]).strip("_")

    def name(self):
        return self.join_parts(self.side, self.base_name, *self.labels)
