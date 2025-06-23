from maya import cmds
from typing import Dict
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.guides.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.constant.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.base.jointchain import LimbJointChainSetup


class LimbResultComponent:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.module = ModuleInfo(guide)
        self.map: Dict = {}
        self.group: str = None

    def create(self):
        # Step 0: Create result Module Group
        group_name = limb_level_format(PJ, RESULT, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.group = cmds.group(em=True, name=group_name)
            cmds.xform(self.group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # Step 1 : Create result joint chain
        result_joint_chain = LimbJointChainSetup(self.guide.name, RESULT)
        result_joint_chain.build()
        cmds.parent(result_joint_chain.group, self.group)

        # Step 2 : Create connection nodes
        for guide in self.module.guides + self.module.guides_end:
            result_joint = result_joint_chain.output.get(guide.name)
            pairblend_name = limb_level_format(PJ, RESULT, guide.side, guide.name_raw, level=None, item=PAIRBLEND)
            blendcolor_name = limb_level_format(PJ, RESULT, guide.side, guide.name_raw, level=None, item=SCALEBLEND)
            pair_blend = cmds.createNode("pairBlend", name=pairblend_name)
            scale_blend = cmds.createNode("blendColors", name=blendcolor_name)

            # Step 3 : Map result joints and connection nodes
            self.map[guide.name] = {JNT: result_joint, PAIRBLEND: pair_blend, SCALEBLEND: scale_blend}
