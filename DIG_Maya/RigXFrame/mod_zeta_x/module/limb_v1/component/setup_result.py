from maya import cmds
from typing import List
from galang_utils.rig_x_frame.constants.project import role as role
from galang_utils.rig_x_frame.core.guide import ModuleInfo
from rig_x_frame.mod_zero.base.component.dag import Node

from galang_utils.rig_x_frame.mod_zero.base.component.group import GroupNode
from core.component.joint import JointSet


class LimbResultComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.guides = module.guides
        self.group = GroupNode(self.guide, module, role.RESULT, [role.RIG, role.GROUP])
        self.joints = JointSet(self.guides, module, role.RESULT)

    def create(self):
        # Step 0: Create result components
        components: List[Node] = [self.group, self.joints]
        for component in components:
            component.create()
