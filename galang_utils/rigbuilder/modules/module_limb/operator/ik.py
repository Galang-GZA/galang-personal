from maya import cmds
from typing import Dict
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_limb.rule.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.component.zcomponent import *


class LimbIKOperator:
    def __init__(self, component: LimbComponent):
        self.component = component
        self.module = component.ik.module
        self.map: Dict = {}

    def run(self):
        ik_map = self.component.ik.map
        for index, guide in enumerate(self.module.guides + self.module.guides_end):
            ik_control = ik_map[guide.name][CTRL].ctrl
            ik_joint = ik_map[guide.name][JNT]

            if index == 0:
                cmds.pointConstraint(ik_control, ik_joint)
                cmds.scaleConstraint(ik_control, ik_joint)
            if index == 1:
                cmds.poleVectorConstraint(ik_control, self.component.ik.handle)
            if index == 2:
                cmds.orientConstraint(ik_control, ik_joint)
                cmds.scaleConstraint(ik_control, ik_joint)
