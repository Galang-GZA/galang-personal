from typing import List
from maya import cmds

from galang_utils.rig_x_frame.constants.project import role as role
from galang_utils.rig_x_frame.constants.project import setup as setup

from galang_utils.rig_x_frame.core.guide import ModuleInfo
from rig_x_frame.mod_zero.base.component.dag import Node
from rig_x_frame.mod_zero.limb.component.detail import DetailComponent


class LimbDetailComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.guides = module.guides

        # Pre-compute group detail rig group node
        self.group = Node(self.guide, module, [role.DETAIL, role.RIG, role.GROUP])
        self.upper = DetailComponent(module, setup.SUB_DIVS, 0)
        self.lower = DetailComponent(module, setup.SUB_DIVS, 1)

    def create(self):
        self.__create_pre_computed_components()
        self.__parent_details_to_rig_group()

    def __create_pre_computed_components(self):
        components: List[Node] = [self.group, self.upper, self.lower]
        for component in components:
            component.create()

    def __parent_details_to_rig_group(self):
        detail_components = [self.upper, self.lower]
        for component in detail_components:
            cmds.parent(component.group, self.group)
