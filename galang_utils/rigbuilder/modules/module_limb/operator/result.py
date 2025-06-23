from maya import cmds
from typing import Dict
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_limb.constant.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.component.zcomponent import *


class LimbResultOperator:
    def __init__(self, component: LimbComponent):
        self.component = component
        self.module = component.result.module
        self.map: Dict = {}

    def run(self):
        ik_map = self.component.ik.map
        fk_map = self.component.fk.map
        result_map = self.component.result.map

        for guide in self.module.guides + self.module.guides_end:
            ik_joint = ik_map[guide.name][JNT]
            fk_joint = fk_map[guide.name][JNT]
            result_joint = result_map[guide.name][JNT]
            pair_blend = result_map[guide.name][PAIRBLEND]
            scale_blend = result_map[guide.name][SCALEBLEND]

            connections = [
                (ik_joint, "translate", pair_blend, "inTranslate1"),
                (ik_joint, "rotate", pair_blend, "inRotate1"),
                (ik_joint, "scale", scale_blend, "color2"),
                (fk_joint, "translate", pair_blend, "inTranslate2"),
                (fk_joint, "rotate", pair_blend, "inRotate2"),
                (fk_joint, "scale", scale_blend, "color1"),
                (pair_blend, "outTranslate", result_joint, "translate"),
                (pair_blend, "outRotate", result_joint, "rotate"),
                (scale_blend, "output", result_joint, "scale"),
            ]
            for scr_node, scr_attr, dst_node, dst_attr in connections:
                cmds.connectAttr(f"{scr_node}.{scr_attr}", f"{dst_node}.{dst_attr}")

            cmds.setAttr(f"{pair_blend}.weight", 0.5)
