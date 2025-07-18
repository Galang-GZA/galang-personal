from maya import cmds
from typing import Dict, List
from galang_utils.rigbuilder.constant.project import role as P_ROLE
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupCreator



class LimbContainerComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.groups: Dict = {}

    def create(self):
        grp_types = [P_ROLE.SYSTEM, P_ROLE.STASIS, P_ROLE.CONSTRAINT]
        core_grp = LimbGroupCreator(grp_types, self.module)
        core_grp.create()
        self.groups = core_grp.map
