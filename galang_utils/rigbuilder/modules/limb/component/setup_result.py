from maya import cmds
from typing import List
from galang_utils.rigbuilder.constants.project import role as role
from galang_utils.rigbuilder.cores.guide import ModuleInfo
from rigbuilder.modules.base.component.dag import Node

from galang_utils.rigbuilder.modules.base.component.group import GroupNode
from rigbuilder.modules.base.component.joint_chain import JointChain


class LimbResultComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.guides = module.guides
        self.group = GroupNode(self.guide, module, role.RESULT, [role.RIG, role.GROUP])
        self.joints = JointChain(self.guides, module, role.RESULT)

    def create(self):
        # Step 0: Create result components
        components: List[Node] = [self.group, self.joints]
        for component in components:
            component.create()
