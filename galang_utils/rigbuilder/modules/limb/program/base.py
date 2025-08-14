from typing import List
from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.constant.project import setup as setup
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat


class LimbBaseNode(str):
    """
    Base class for programs
    """

    def __new__(
        cls,
        guide: GuideInfo,
        module: ModuleInfo,
        kinematics: str,
        types: List = [],
        index: int = None,
    ):
        format = LimbFormat(module.side, kinematics)
        name = format.name(guide.name_raw, types, index)
        return super().__new__(cls, name)

    def __init__(
        self,
        guide: GuideInfo,
        module: ModuleInfo,
        kinematics: str,
        types: List = None,
        level: str = None,
        position: List[float] = None,
        orientation: List[float] = None,
    ):
        self.types = types
        self.level = level
        self.guide = guide
        self.module = module
        self.kinematics = kinematics
        self.position = self._fallback(position, guide.position)
        self.orientation = self._fallback(orientation, guide.orientation)

    def _fallback(val, default):
        return default if val is None else val

    def create():
        pass
