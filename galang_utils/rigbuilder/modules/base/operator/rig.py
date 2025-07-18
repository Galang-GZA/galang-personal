from maya import cmds
from typing import Dict
from galang_utils.rigbuilder.constant.constant_general import *
from galang_utils.rigbuilder.constant.constant_project import *
from galang_utils.rigbuilder.modules.base.rule.constant_module import *
from galang_utils.rigbuilder.modules.base.component.zcomponent import *


class BaseRigOperator:
    def __init__(self, component: BaseComponent):
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
                cmds.scaleConstraint(fk_control, fk_joint)
