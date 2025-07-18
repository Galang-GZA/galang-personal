"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from galang_utils.rigbuilder.constant.constant_general import *
from galang_utils.rigbuilder.constant.constant_project import *
from galang_utils.rigbuilder.modules.finger.constant import *
from galang_utils.rigbuilder.modules.finger.guide import Finger_GuideInfo, Finger_GuideList
from galang_utils.rigbuilder.modules.finger.controls import Finger_ControlCreator
from galang_utils.rigbuilder.modules.finger.jointchain import Finger_JointChainSetup
from galang_utils.rigbuilder.modules.finger.kinematics import Finger_IKSetup, Finger_FKSetup


class Finger_ModuleBuilder:
    def __init__(self, guide):
        self.guide = Finger_GuideInfo(guide)
        self.input = Finger_GuideList(guide)
        self.result_joint = Finger_JointChainSetup(guide, RESULT)
        self.fk = Finger_FKSetup(guide)
        self.ik = Finger_IKSetup(guide)
        self.module_group = None
        self.module_map = {}

    def build(self):
        # Step 0: Create Module Group
        group_name = finger_level_format(PROJECT, self.guide.module, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.module_group = cmds.group(em=True, name=group_name)
            cmds.xform(self.module_group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # Step 1: Build FK
        self.fk.build()

        # Step 2: Parent Items under Module Group
        cmds.parent(self.fk.fk_module_group, self.module_group)
