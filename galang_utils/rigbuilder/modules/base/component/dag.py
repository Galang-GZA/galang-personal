from typing import List
from rigbuilder.constant.project import role as role
from rigbuilder.constant.project import setup as setup
from rigbuilder.core.guide import GuideInfo, ModuleInfo
from rigbuilder.modules.limb.constant.format import LimbFormat


class Node(str):
    """
    Base class for programs
    """

    def __new__(
        cls,
        guide: GuideInfo,
        module: ModuleInfo,
        types: List = None,
    ):
        format = LimbFormat(module.side)
        name = format.name(guide.name_raw, types)
        return super().__new__(cls, name)

    def __init__(
        self,
        guide: GuideInfo,
        module: ModuleInfo,
        types: List = None,
        position: List[float] = None,
    ):
        self.types = types
        self.guide = guide
        self.module = module
        self.position = self._fallback(position, guide.position)
        self.orientation = guide.orientation

    def _fallback(val, default):
        return default if val is None else val

    def create():
        pass
