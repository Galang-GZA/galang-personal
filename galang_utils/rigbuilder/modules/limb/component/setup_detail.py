from typing import List

from galang_utils.rigbuilder.constants.project import role as role
from galang_utils.rigbuilder.constants.project import setup as setup

from galang_utils.rigbuilder.cores.guide import ModuleInfo
from rigbuilder.modules.base.component.dag import Node
from galang_utils.rigbuilder.modules.base.component.group import GroupNode
from galang_utils.rigbuilder.modules.base.component.detail import DetailComponent


class LimbDetailComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.guides = module.guides

        # Pre-compute group detail rig group node
        self.group = GroupNode(self.guide, module, [role.DETAIL, role.RIG, role.GROUP])
        self.upper = DetailComponent(module, setup.SUB_DIVS, 0)
        self.lower = DetailComponent(module, setup.SUB_DIVS, 1)

    def create(self):
        components: List[Node] = [self.group, self.upper_detail, self.lower_detail]
        for component in components:
            component.create()
