"""THIS CONSTANT IS TO BE CHANGED BASED ON THE MODULE NEEDS"""

from typing import List
from galang_utils.rigbuilder.constant.project import role as role


class LimbFormat:
    def __init__(self, side, kinematics):
        self.kinematics = kinematics
        self.side = side

    @staticmethod
    def join_parts(*parts):
        return "_".join([p for p in parts if p]).strip("_")

    def name(self, name: str, types: List = None, i: int = None):
        index_part = f"{i+1:02d}" if i is not None else None
        type_parts = types if types else []
        return self.join_parts(role.PROJECT, self.kinematics, self.side, name, *type_parts, index_part)

    @staticmethod
    def name_static(side: str, kinematics: str, name: str, types: List = None, i: int = None):
        index_part = f"{i+1:02d}" if i is not None else None
        type_parts = types if types else []
        return LimbFormat.join_parts(role.PROJECT, kinematics, side, name, *type_parts, index_part)
