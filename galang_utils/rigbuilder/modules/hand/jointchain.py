"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.hand.constant import *
from galang_utils.rigbuilder.modules.hand.guide import Hand_GuideInfo, Hand_GuideList


class Hand_JointChainSetup:
    def __init__(self, guide, kinematics):
        self.guide = Hand_GuideInfo(guide)
        self.input = Hand_GuideList(guide)
        self.kinematics = kinematics
        self.joints_created = {}
        self.group = None

    def build(self):
        group_name = hand_level_format(PROJECT, self.kinematics, self.guide.side, self.guide.name_raw, GROUP, JNT)
        if not cmds.objExists(group_name):
            self.group = cmds.group(empty=True, name=group_name)
            cmds.xform(self.group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")
        cmds.hide(self.group)

        for g in self.input.guides:
            if g.is_guide_end or g.is_guide_misc:
                continue
            if not g.module == ROOT:
                module_contents: Dict = MODULE_MAP.get(self.guide.module, {}).get("contents", [])
                if g.module not in module_contents:
                    continue

            joint_name = hand_joint_format(PROJECT, self.kinematics, g.side, g.name_raw, JNT)
            if cmds.objExists(joint_name):
                cmds.warning(f"{joint_name} is already created. Skipppz")
                continue

            cmds.select(clear=True)
            jnt = cmds.joint(
                name=hand_joint_format(PROJECT, self.kinematics, g.side, g.name_raw, JNT),
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
