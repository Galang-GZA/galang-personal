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
        self.kinematics = NK
        self.hand_control = None
        self.module_control = None
        self.module_group = None
        self.joint_group = None
        self.hand_map = {}
        self.finger_map = {}

    def build(self):
        # Step 0: Create Module Group
        group_name = hand_level_format(PJ, self.guide.module, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.module_group = cmds.group(em=True, name=group_name)
            cmds.xform(self.module_group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        jnt_group_name = hand_level_format(PJ, self.kinematics, self.guide.side, "hand", GROUP, JNT)
        if not cmds.objExists(jnt_group_name):
            self.joint_group = cmds.group(em=True, name=jnt_group_name)
            cmds.xform(self.module_group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # Step 1: Build miscellaneous control
        self.hand_control = Hand_ControlCreator(self.guide.name, self.kinematics, NODE_LOCAL_LEVELS)
        self.hand_control.create()
        self.hand_map[self.guide.name] = {CTRL: self.hand_control, JNT: None}

        # Step 2: Build Carpal and Fingers
        # self.carpal_joint_grp = cmds.group()
        carpal_list = [
            guide.name
            for guide in self.input.guides
            if not guide.name == self.guide.name and not guide.is_guide_end or guide.is_guide_misc
        ]
        carpal_count_ori = len(carpal_list)
        carpal_count_updated = len(carpal_list)

        for guide in self.input.guides:
            if guide.is_guide_end or guide.is_guide_misc:
                continue

            if not guide.name == self.guide.name:
                # Build carpal
                cmds.select(clear=True)
                carpal_control = Hand_ControlCreator(guide.name, self.kinematics, NODE_MAIN_LEVELS)
                carpal_control.create()
                cmds.select(clear=True)
                carpal_joint = cmds.joint(
                    name=hand_joint_format(self.kinematics, NK, guide.side, guide.name_raw, JNT),
                    position=guide.position,
                    orientation=guide.orientation,
                )
                # Parent carpal to hand
                cmds.parent(carpal_control.top, self.module_group)
                cmds.parent(carpal_joint, self.joint_group)

                # Connect hand transform to carpal
                attributes = ["tx", "ty", "tz", "rx", "ry", "rz", "s"]

                for attribute in attributes:
                    if not attribute == "s":
                        transform_divider = carpal_count_updated / carpal_count_ori
                        multiplier = cmds.createNode(
                            "multDoubleLinear",
                            name=hand_misc_format(PJ, self.kinematics, guide.side, guide.name_raw, "MISC", local=None),
                        )
                        cmds.connectAttr(f"{self.hand_control.ctrl}.{attribute}", f"{multiplier}.input1")
                        cmds.connectAttr(f"{multiplier}.output", f"{carpal_control.nodes.get(LINK)}.{attribute}")
                        cmds.setAttr(f"{multiplier}.input2", transform_divider)

                    else:
                        cmds.connectAttr(
                            f"{self.guide.name}.{attribute}", f"{carpal_control.nodes.get(LINK)}.{attribute}"
                        )
                carpal_count_updated = carpal_count_updated - 1

                # Add to module map
                self.hand_map[guide.name] = {CTRL: carpal_control, JNT: carpal_joint}

            # Build Fngers
            fingers = guide.children
            for finger in fingers:
                self.finger = Hand_GuideInfo(finger)
                if self.finger.module_start and self.finger.module == FINGER:
                    finger_setup = Finger_ModuleBuilder(self.finger.name)
                    finger_setup.build()

                    # Parent finger to hand
                    cmds.parent(finger_setup.module_group, self.module_group)
                    print(finger_setup.module_group, self.hand_map[guide.name][CTRL].ctrl)

                    if not guide.name == self.guide.name:
                        cmds.parentConstraint(self.hand_map[guide.name][CTRL].ctrl, finger_setup.module_group, mo=True)
                    self.finger_map[guide]: {MODULE: finger_setup}
