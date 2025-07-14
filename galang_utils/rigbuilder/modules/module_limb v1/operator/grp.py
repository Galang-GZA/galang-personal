from maya import cmds
from typing import Dict
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.constants import constant_project as const_proj
from galang_utils.rigbuilder.modules.module_limb.rule.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.component.zcomponent import *


class LimbGroupOperator:
    def __init__(self, component: LimbComponent):
        self.component = component
        self.module = component.group.module

    def run(self):
        guides = self.module.guides + self.module.guides_end
        grp_system = self.component.group.map[SYSTEM]
        grp_stasis = self.component.group.map[STASIS]
        grp_constraint = self.component.group.map[CONSTRAINT]

        grp_ik = self.component.ik.groups
        grp_fk = self.component.fk.groups
        grp_result = self.component.result.group
        grp_roll = self.component.roll.groups
        grp_setting = self.component.setting.setting.top

        # Step 1 : Parent constraint nodes to their group
        constraint_nodes = cmds.ls("*Constraint1")
        for node in constraint_nodes:
            if self.module.guide.side in node:
                if any(g.name_raw in node for g in guides):
                    cmds.parent(node, grp_constraint)

        # Step 2 : Parent stasis components to their group
        grps_stasis = [grp_ik[JNT], grp_fk[JNT], grp_ik[LOCATOR], grp_ik[DISTANCE], grp_constraint]
        for grp in grps_stasis:
            cmds.parent(grp, grp_stasis)

        # Step 3 : Parent system components to their group
        grps_sys = [grp_ik[MASTER], grp_fk[MASTER], grp_roll[MASTER], grp_result, grp_setting]
        for grp in grps_sys:
            cmds.parent(grp, grp_system)

        # Step 4 : Parent roll components to system group
