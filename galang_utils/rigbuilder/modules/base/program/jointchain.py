"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from typing import Dict, List
from galang_utils.rigbuilder.constant.project import role as P_ROLE
from galang_utils.rigbuilder.modules.base.constant.format import BaseFormat
from galang_utils.rigbuilder.modules.base.program.group import BaseGroupCreator
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo


class BaseJointChainSetup:
    def __init__(self, guide, kinematics=None, create_group=True):
        self.guide = GuideInfo(guide)
        self.module = ModuleInfo(guide)
        self.kinematics = kinematics
        self.create_group = create_group
        self.joints: List = []
        self.group: str = None
        self.format = BaseFormat(self.kinematics, self.guide.side)

    def create(self):
        grp_types = [P_ROLE.GROUP]
        grp = BaseGroupCreator(grp_types, self.module)
        grp.create()
        self.group = grp.map[P_ROLE.GROUP]

        jnt_parent = None
        for g in self.module.guides + self.module.guides_end:
            if g.is_guide_end:
                continue

            joint_name = self.format.name(self.guide.name_raw, P_ROLE.JNT)
            if cmds.objExists(joint_name):
                cmds.warning(f"{joint_name} is already created. Skipppz")
                continue

            cmds.select(clear=True)
            jnt = cmds.joint(name=joint_name, position=g.position, orientation=g.orientation)
            cmds.setAttr(f"{jnt}.side", g.side_id)
            self.joints.append(jnt)
            if not jnt_parent:
                if self.group:
                    cmds.parent(jnt, self.group)
            else:
                cmds.parent(jnt, jnt_parent)
            jnt_parent = jnt
