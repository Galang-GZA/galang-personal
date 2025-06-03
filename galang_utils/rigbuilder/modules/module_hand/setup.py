"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_hand.constant import *
from galang_utils.rigbuilder.modules.module_hand.guide import Hand_GuideInfo, Hand_GuideList
from galang_utils.rigbuilder.modules.module_hand.controls import Hand_ControlCreator
from galang_utils.rigbuilder.modules.module_hand.jointchain import Hand_JointChainSetup
from galang_utils.rigbuilder.modules.module_hand.kinematics import Hand_FKSetup

from galang_utils.rigbuilder.modules.module_finger.zpackage import *


class Hand_ModuleBuilder:
    def __init__(self, guide):
        self.guide = Hand_GuideInfo(guide)
        self.input = Hand_GuideList(guide)
        self.result_joint = Hand_JointChainSetup(guide, RESULT)
        self.module_control = None
        self.limb_module_group = None
        self.limb_module_blend_map = {}

    def build(self):
        # Step 0: Create Module Group
        group_name = hand_level_format(PJ, self.guide.module, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.limb_module_group = cmds.group(em=True, name=group_name)
            cmds.xform(self.limb_module_group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # Step 1: Build miscellaneous control
        self.module_control = Hand_FKSetup(self.guide.name, NK)
        self.module_control.build()

        for g in self.input.guides:
            if g.module_start and g.module == FINGER:
                self.finger = Finger_ModuleBuilder(g.name)
                self.finger.build()
                # print(g.name)
