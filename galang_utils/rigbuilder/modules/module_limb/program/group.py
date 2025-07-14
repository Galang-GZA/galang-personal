from maya import cmds
from typing import Dict, List
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_limb.constants.format import LimbFormat
from galang_utils.rigbuilder.core.guide import ModuleInfo


class LimbGroupCreator:
    def __init__(self, grp_types, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.grp_types: List = grp_types
        self.map: Dict = []

    def create(self):
        for type in self.grp_types:
            grp_name = LimbFormat.level(PROJECT, "", self.guide.side, self.guide.name_raw, type)
            if not cmds.objExists(grp_name):
                self.map[type] = cmds.group(em=True, name=grp_name)
                cmds.xform(self.map[type], t=self.guide.position, ro=self.guide.orientation)
