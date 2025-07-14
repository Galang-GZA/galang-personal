"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from typing import Dict, List
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_limb.constants.format import LimbFormat
from galang_utils.rigbuilder.modules.module_limb.program.group import LimbGroupCreator
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo


class LimbJointChainSetup:
    def __init__(self, guide, kinematics=None, create_group=True):
        self.guide = GuideInfo(guide)
        self.module = ModuleInfo(guide)
        self.kinematics = kinematics
        self.create_group = create_group
        self.output: List = []
        self.group: str = None

    def create(self):
        grp_types = [GROUP]
        grp = LimbGroupCreator(grp_types, self.module)
        grp.create()
        self.group = grp.map[GROUP]

        jnt_parent = None
        for g in self.module.guides + self.module.guides_end:
            if g.is_guide_end:
                continue

            joint_name = LimbFormat.level(PROJECT, self.kinematics, g.side, g.name_raw, JNT)
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
