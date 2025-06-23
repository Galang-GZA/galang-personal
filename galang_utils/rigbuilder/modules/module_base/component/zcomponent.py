from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.module_base.component.bind import BaseBindComponent
from galang_utils.rigbuilder.modules.module_base.component.rig import BaseRigComponent


class BaseComponent:
    def __init__(self, module: ModuleInfo):
        self.bind = BaseBindComponent(module)
        self.fk = BaseRigComponent(module)

    def create_bind(self):
        self.bind.create()

    def create_fk(self):
        self.fk.create()
