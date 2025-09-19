from typing import List
from rig_x_frame.core.guide import ModuleInfo
from rig_x_frame.mod_zero.base.component.dag import Node
from rig_x_frame.mod_zero.base.component.setup_group import GroupComponent
from rig_x_frame.mod_zero.base.component.setup_bind import BindComponent
from rig_x_frame.mod_zero.base.component.setup_fk import FKComponent


class Components:
    def __init__(self, module: ModuleInfo, create_rig: bool = True):
        self.module = module
        self.create_rig = create_rig

        self.group = GroupComponent(module)
        self.bind = BindComponent(module)
        self.fk = FKComponent(module)

    def create(self):
        self.create_bind_components()
        if self.create_rig:
            self.create_rig_components()

    def create_rig_components(self):
        rig_components: List[Node] = [self.group, self.fk]
        for component in rig_components:
            component.create()

    def create_bind_components(self):
        self.bind.create()
