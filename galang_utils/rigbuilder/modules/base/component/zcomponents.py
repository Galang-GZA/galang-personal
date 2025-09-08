from typing import List
from rigbuilder.cores.guide import ModuleInfo
from rigbuilder.modules.base.component.dag import Node
from rigbuilder.modules.base.component.setup_group import GroupComponent
from rigbuilder.modules.base.component.setup_bind import BindComponent
from rigbuilder.modules.base.component.setup_fk import FKComponent


class Components:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.group = GroupComponent(module)
        self.bind = BindComponent(module)
        self.fk = FKComponent(module)
        self.bind_driver = self.fk.joints

    def create(self):
        components: List[Node] = [self.bind, self.fk]
        for component in components:
            component.create()
