from maya import cmds
from typing import Dict
from galang_utils.curve.shapes_library import *
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
        ik_joint_chain = LimbJointChainSetup(self.guide.name, RESULT)
        cmds.parent(ik_joint_chain.group, self.group)

        # Step 2 : Map result joints
        self.map = ik_joint_chain.output
