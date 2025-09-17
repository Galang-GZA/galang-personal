"""THIS CONSTANT IS TO BE CHANGED BASED ON THE MODULE NEEDS"""

from typing import List
from galang_utils.rigbuilder.constants.project import role as role


class Format:
    def __init__(self, side, raw_name: str, types: List = None):
        self.side = side
        self.raw_name = raw_name
        self.types = types

    @staticmethod
    def join_parts(*parts):
        return "_".join([p for p in parts if p]).strip("_")

    def name(self):
        return self.join_parts(role.PROJECT, self.side, self.raw_name, *self.types)
