from typing import List
from rig_x_frame.constants.project import role as role
from rig_x_frame.constants.project import setup as setup
from rig_x_frame.core.guide import GuideInfo, ModuleInfo
from rig_x_frame.mod_zero.base.constant.format import Format


"""PERTIMBANGKAN BUAT TARUH DI LUAR RIG BUILDER"""


class Node(str):
    def __new__(cls, guide: GuideInfo, module: ModuleInfo, types: List):
        format = Format(module.side)
        name = format.name(guide.name_raw, types)
        return super().__new__(cls, name)

    def __init__(self, guide: GuideInfo, module: ModuleInfo, types: List, position: List[float] = None):
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
        self.types = types
        self.guide = guide
        self.module = module
        self.position = self._fallback(position, guide.position)
        self.orientation = guide.orientation

    def _fallback(val, default):
        return default if val is None else val

    def create():
        "GANTI PENULISAN BIAR KE TRANSFORM NODE"
        """
        Creates an empty Maya group at the given position & orientation.
        """
        # grp_node = cmds.group(em=True, name=self)
        # cmds.xform(grp_node, t=self.position, ro=self.orientation)
