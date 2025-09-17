from typing import List
from maya import cmds


from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup
from rigbuilder.modules.base.constant.format import Format


"""PERTIMBANGKAN BUAT TARUH DI LUAR RIG BUILDER"""


class Node(str):
    def __new__(cls, guide_name: str, side: str, types: List):
        name_format = Format(side, guide_name, types).name()
        return super().__new__(cls, name_format)

    def __init__(self, guide_name: str, side: str, types: List, position: List[float], orientation: List[float]):
        # Attributes
        self.translate_x = f"{self}.translateX"
        self.translate_y = f"{self}.translateY"
        self.translate_z = f"{self}.translateZ"
        self.rotate_x = f"{self}.rotateX"
        self.rotate_y = f"{self}.rotateY"
        self.rotate_z = f"{self}.rotateZ"
        self.scale_x = f"{self}.scaleX"
        self.scale_y = f"{self}.scaleY"
        self.scale_z = f"{self}.scaleZ"
        self.visibility = f"{self}.visibility"
        self.worldPosition_0 = f"{self}.worldPosition[0]"

        # Data
        self.side = side
        self.types = types
        self.guide = guide_name
        self.position = position
        self.orientation = orientation

    def create(self):
        # Creates an empty Maya group at the given position & orientation.
        transform_node = cmds.group(em=True, name=self)
        cmds.xform(transform_node, t=self.position, ro=self.orientation)
