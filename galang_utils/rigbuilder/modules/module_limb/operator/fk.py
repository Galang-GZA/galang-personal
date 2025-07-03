from maya import cmds
from typing import Dict
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_limb.rule.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.component.zcomponent import *


class LimbFKOperator:
    def __init__(self, component: LimbComponent):
        self.component = component
        self.module = component.fk.module
        self.map: Dict = {}

    def run(self):
        fk_map = self.component.fk.map
        for guide in self.module.guides + self.module.guides_end:
            fk_control = fk_map[guide.name][CTRL].ctrl
            fk_joint = fk_map[guide.name][JNT]

            if fk_control and fk_joint:
                cmds.parentConstraint(fk_control, fk_joint)
                cmds.scaleConstraint(fk_control, fk_joint, mo=True)
