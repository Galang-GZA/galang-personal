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
            print(guide.name)
            ik_joint = ik_map[guide.name][JNT]
            fk_joint = fk_map[guide.name][JNT]
            result_joint = result_map.get(guide.name)

            pairblend_name = limb_level_format(PJ, RESULT, guide.side, guide.name_raw, level=None, item=PAIRBLEND)
            blendcolor_name = limb_level_format(PJ, RESULT, guide.side, guide.name_raw, level=None, item=SCALEBLEND)
            pair_blend = cmds.createNode("pairBlend", name=pairblend_name)
            scale_blend = cmds.createNode("blendColors", name=blendcolor_name)

            cmds.connectAttr(f"{ik_joint}.translate", f"{pair_blend}.inTranslate1")
            cmds.connectAttr(f"{ik_joint}.rotate", f"{pair_blend}.inRotate1")
            cmds.connectAttr(f"{ik_joint}.scale", f"{scale_blend}.color2")

            cmds.connectAttr(f"{fk_joint}.translate", f"{pair_blend}.inTranslate2")
            cmds.connectAttr(f"{fk_joint}.rotate", f"{pair_blend}.inRotate2")
            cmds.connectAttr(f"{fk_joint}.scale", f"{scale_blend}.color1")

            cmds.connectAttr(f"{pair_blend}.outTranslate", f"{result_joint}.translate")
            cmds.connectAttr(f"{pair_blend}.outRotate", f"{result_joint}.rotate")
            cmds.connectAttr(f"{scale_blend}.output", f"{result_joint}.scale")

            cmds.setAttr(f"{pair_blend}.weight", 0.5)
