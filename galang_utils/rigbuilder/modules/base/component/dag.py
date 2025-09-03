from typing import List
from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup
from rigbuilder.cores.guide import GuideInfo, ModuleInfo
from rigbuilder.modules.base.constant.format import Format


class Node(str):
    def __new__(cls, guide: GuideInfo, module: ModuleInfo, types: List):
        format = Format(module.side)
        name = format.name(guide.name_raw, types)
        return super().__new__(cls, name)

    def __init__(self, guide: GuideInfo, module: ModuleInfo, types: List, position: List[float] = None):
        self.types = types
        self.guide = guide
        self.module = module
        self.position = self._fallback(position, guide.position)
        self.orientation = guide.orientation

    def _fallback(val, default):
        return default if val is None else val

    def create():
        pass
