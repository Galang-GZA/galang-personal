"""THIS CONSTANT IS TO BE CHANGED BASED ON THE MODULE NEEDS"""

from typing import List
from galang_utils.rig_x_frame.constants.project import role as role


class LimbFormat:
    def __init__(self, side):
        self.side = side

    @staticmethod
    def join_parts(*parts):
        return "_".join([p for p in parts if p]).strip("_")

    def name(self, name: str, types: List = None):
        type_parts = types if types else []
        return self.join_parts(role.PROJECT, self.side, name, *type_parts)

    @staticmethod
    def name_static(side: str, name: str, types: List = None):
        type_parts = types if types else []
        return LimbFormat.join_parts(role.PROJECT, side, name, *type_parts)
