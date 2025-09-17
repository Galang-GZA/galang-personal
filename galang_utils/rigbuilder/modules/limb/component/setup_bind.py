from maya import cmds
from typing import List

from rigbuilder.cores.guide import ModuleInfo
from rigbuilder.programs.sub_position import SubPositions

from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup

from rigbuilder.modules.base.component.dag import Node
from core.component.joint import JointSet
from rigbuilder.modules.base.component.setup_bind import BindComponent


class LimbBindComponent(BindComponent):
    def __init__(self, module: ModuleInfo, sub: bool = True):
        super().__init__(module)
        self.module = module
        self.sub = sub

        if sub:
            sub_types = [role.BIND, role.SUB, setup.INDEX]
            upper_guides = [self.module.guides[0] * setup.SUB_DIVS]
            lower_guides = [self.module.guides[1] * setup.SUB_DIVS]
            upper_sub_positions = SubPositions(self.module, setup.SUB_DIVS, 0).get()
            lower_sub_positions = SubPositions(self.module, setup.SUB_DIVS, 1).get()

            # Pre compute sub joints
            self.upper_sub_joints = JointSet(upper_guides, self.module, sub_types, upper_sub_positions)
            self.lower_sub_joints = JointSet(lower_guides, self.module, sub_types, lower_sub_positions)

    def create(self):
        self.__create_bind_components()
        if self.sub:
            self.__create_and_parent_sub_joints

    def __create_and_parent_sub_joints(self):
        sub_joints = [self.upper_sub_joints, self.lower_sub_joints]
        for i in range(2):
            sub_joints[i].create()
            for sub_joint in sub_joints[i]:
                cmds.parent(sub_joint, self.joints[i])
