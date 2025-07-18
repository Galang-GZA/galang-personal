from maya import cmds
from typing import Dict, List
from galang_utils.rigbuilder.modules.base.constant.format import BaseFormat
from galang_utils.rigbuilder.core.guide import ModuleInfo


class BaseGroupCreator:
    def __init__(self, grp_types, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.grp_types: List = grp_types
        self.map: Dict = []
        self.format = BaseFormat(None, self.guide.side)

    def create(self):
        for type in self.grp_types:
            grp_name = self.format.name(self.guide.name_raw, type)
            if not cmds.objExists(grp_name):
                self.map[type] = cmds.group(em=True, name=grp_name)
                cmds.xform(self.map[type], t=self.guide.position, ro=self.guide.orientation)
