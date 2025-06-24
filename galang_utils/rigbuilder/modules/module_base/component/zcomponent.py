from typing import Dict
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.module_base.component.bind import BaseBindComponent
from galang_utils.rigbuilder.modules.module_base.component.rig import BaseRigComponent


class BaseComponent:
    def __init__(self, module: ModuleInfo):
        self.bind = BaseBindComponent(module)
        self.rig = BaseRigComponent(module)
        self.bind_connection: Dict = {}

    def create_bind(self):
        self.bind.create()

    def create_rig(self):
        self.rig.create()

        # Add result joints to bind connection
        for guide, data in self.rig.map.items():
            self.bind_connection[guide] = data[JNT]
