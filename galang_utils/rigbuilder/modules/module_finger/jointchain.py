"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_finger.constant import *
from galang_utils.rigbuilder.modules.module_finger.guide import Finger_GuideInfo, Finger_GuideList


class Finger_JointChainSetup:
    def __init__(self, guide, kinematics):
        self.guide = Finger_GuideInfo(guide)
        self.input = Finger_GuideList(guide)
        self.joints_created = {}
        self.kinematics = kinematics
        self.group = None

    def build(self):
        group_name = finger_level_format(PROJECT, self.kinematics, self.guide.side, self.guide.name_raw, GROUP, JNT)
        if not cmds.objExists(group_name):
            self.group = cmds.group(empty=True, name=group_name)
            cmds.xform(self.group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")
        cmds.hide(self.group)

        for g in self.input.guides:
            if g.is_guide_end or g.is_guide_misc:
                continue

            # if g.module_start:
            #     joint_name = name_format(self.kinematics, g.side, g.parent)
            # else:
            #     joint_name = name_format(self.kinematics, g.side, g.name_raw)
            joint_name = finger_joint_format(PROJECT, self.kinematics, g.side, g.name_raw, JNT)
            if cmds.objExists(joint_name):
                cmds.warning(f"{joint_name} is already created. Skipppz")
                continue

            cmds.select(clear=True)
            jnt = cmds.joint(
                name=finger_joint_format(PROJECT, self.kinematics, g.side, g.name_raw, JNT),
                position=g.position,
                orientation=g.orientation,
            )
            cmds.setAttr(f"{jnt}.type", g.module_id)
            cmds.setAttr(f"{jnt}.side", g.side_id)
            self.joints_created[g.name] = jnt
            if g.name_raw == self.guide.name_raw:
                cmds.parent(jnt, self.group)
            # print(f"Created joint: {jnt}")

        for g in self.input.guides:
            if g.parent:
                child = self.joints_created.get(g.name)
                parent = self.joints_created.get(g.parent)
                if child and parent:
                    cmds.parent(child, parent)
