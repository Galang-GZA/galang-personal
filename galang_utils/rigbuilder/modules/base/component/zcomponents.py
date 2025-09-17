from typing import List
from rigbuilder.cores.guide import ModuleInfo
from rigbuilder.modules.base.component.dag import Node
from rigbuilder.modules.base.component.setup_group import GroupComponent
from rigbuilder.modules.base.component.setup_bind import BindComponent
from rigbuilder.modules.base.component.setup_fk import FKComponent


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
