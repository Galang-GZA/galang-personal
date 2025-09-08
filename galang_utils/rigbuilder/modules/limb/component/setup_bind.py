from maya import cmds
from typing import List

from rigbuilder.cores.guide import ModuleInfo
from rigbuilder.programs.sub_position import SubPositions

from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup

from rigbuilder.modules.base.component.dag import Node
from rigbuilder.modules.base.component.joint_chain import JointChain
from rigbuilder.modules.base.component.setup_bind import BindComponent


class LimbBindComponent(BindComponent):
    def __init__(self, module: ModuleInfo):
        super().__init__(module)

        sub_types = [role.BIND, role.SUB, setup.INDEX]
        upper_guides = [module.guides[0] * setup.SUB_DIVS]
        lower_guides = [module.guides[1] * setup.SUB_DIVS]
        upper_positions = SubPositions(module, setup.SUB_DIVS, 0).get()
        lower_positions = SubPositions(module, setup.SUB_DIVS, 1).get()

        # Pre compute sub joints
        self.upper_sub_joints = JointChain(upper_guides, module, sub_types, upper_positions)
        self.lower_sub_joints = JointChain(lower_guides, module, sub_types, lower_positions)

    def create(self):
        # Step 0 : Create bind joint chain
        components: List[Node] = [self.joints, self.upper_sub_joints, self.lower_sub_joints]
        for component in components:
            component.create()

        sub_joints = [self.upper_sub_joints, self.lower_sub_joints]
        for i in range(2):
            for sub_joint in sub_joints[i]:
                cmds.parent(sub_joint, self.joints[i])
