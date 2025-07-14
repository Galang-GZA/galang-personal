from maya import cmds
from typing import Dict
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_limb.rule.constant_module import *
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.program.group import LimbGroupCreator


class LimbGroupComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.groups: Dict = {}

    def create(self):
        grp_types = [SYSTEM, STASIS, CONSTRAINT]
        fk_grp = LimbGroupCreator(grp_types, self.module)
        fk_grp.create()
        self.groups = fk_grp.map
