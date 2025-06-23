"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_limb.constant.constant_module import *
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo


class LimbJointChainSetup:
    def __init__(self, guide, kinematics=None, create_group=True):
        self.guide = GuideInfo(guide)
        self.module = ModuleInfo(guide)
        self.output = {}
        self.kinematics = kinematics
        self.create_group = create_group
        self.group = None

    def build(self):
        group_name = limb_level_format(PJ, self.kinematics, self.guide.side, self.guide.name_raw, GROUP, JNT)
        if not cmds.objExists(group_name):
            if self.create_group:
                self.group = cmds.group(empty=True, name=group_name)
                cmds.xform(self.group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")
        cmds.hide(self.group)

        jnt_parent = None
        for g in self.module.guides + self.module.guides_end:
            if g.is_guide_end:
                continue

            joint_name = limb_joint_format(PJ, self.kinematics, g.side, g.name_raw, JNT)
            if cmds.objExists(joint_name):
                cmds.warning(f"{joint_name} is already created. Skipppz")
                continue

            cmds.select(clear=True)
            jnt = cmds.joint(name=joint_name, position=g.position, orientation=g.orientation)
            cmds.setAttr(f"{jnt}.side", g.side_id)
            self.output[g.name] = jnt
            if not jnt_parent:
                if self.group:
                    cmds.parent(jnt, self.group)
            else:
                cmds.parent(jnt, jnt_parent)
            jnt_parent = jnt
