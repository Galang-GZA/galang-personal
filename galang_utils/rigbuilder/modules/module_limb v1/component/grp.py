from maya import cmds
from typing import Dict, Union
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_limb.rule.constant_module import *
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo


class LimbGroupComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.map: Dict = {}

    def create(self):
        grp_system = limb_format(PROJECT, "", self.guide.side, self.guide.name_raw, SYSTEM)
        grp_stasis = limb_format(PROJECT, "", self.guide.side, self.guide.name_raw, STASIS)
        grp_constraints = limb_format(PROJECT, "", self.guide.side, self.guide.name_raw, CONSTRAINT)

        grp_names = [grp_system, grp_stasis, grp_constraints]
        grp_types = [SYSTEM, STASIS, CONSTRAINT]

        for name, type in zip(grp_names, grp_types):
            if not cmds.objExists(name):
                grp = cmds.group(em=True, n=name)
                self.map[type] = grp

                if type in [STASIS, CONSTRAINT]:
                    cmds.hide(grp)
