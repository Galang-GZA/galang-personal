from maya import cmds
from typing import Dict
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_limb.constant.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.component.zcomponent import *


class LimbBindOperator:
    def __init__(self, component: LimbComponent):
        self.component = component
        self.module = component.bind.module
        self.map: Dict = {}

    def run(self):
        bind_map = self.component.bind.map
        result_map = self.component.result.map
        for guide in self.module.guides + self.module.guides_end:
            bind_jnt = bind_map.get(guide.name)
            result_jnt = result_map[guide.name][JNT]

            if bind_jnt and result_jnt:
                cmds.parentConstraint(result_jnt, bind_jnt)
                cmds.scaleConstraint(result_jnt, bind_jnt)
