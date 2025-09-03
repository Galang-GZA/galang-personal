from maya import cmds
from typing import List
from galang_utils.rigbuilder.constants.project import role as role
from rigbuilder.modules.base.component.dag import Node
from galang_utils.rigbuilder.cores.guide import ModuleInfo
from galang_utils.rigbuilder.modules.base.component.group import GroupNode
from galang_utils.rigbuilder.modules.base.component.control import ControlSet
from rigbuilder.modules.base.component.joint_chain import JointChain


class FKComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.guides = module.guides
        self.group = GroupNode(self.guide, module, [role.FK, role.RIG, role.GROUP])
        self.joints = JointChain(self.guides, module, [role.FK])
        self.controls = ControlSet(self.guides, module, [role.FK])

    def create(self):
        # Step 0: Create FK components
        components: List[Node] = [self.group, self.joints, self.controls]
        for component in components:
            component.create()
