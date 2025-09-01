from typing import List
from rigbuilder.core.guide import ModuleInfo
from rigbuilder.modules.base.component.dag import Node
from rigbuilder.modules.base.component.setup_bind import BindComponent
from rigbuilder.modules.base.component.setup_ik import IKComponent
from rigbuilder.modules.base.component.setup_fk import FKComponent


class BaseComponent:
    def __init__(self, module: ModuleInfo):
        self.bind = BindComponent(module)
        self.ik = IKComponent(module)
        self.fk = FKComponent(module)

    def create(self):
        components: List[Node] = [self.bind, self.ik, self.fk]
        for component in components:
            component.create()
