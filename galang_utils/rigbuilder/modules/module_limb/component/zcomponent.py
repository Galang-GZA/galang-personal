from typing import Dict
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.module_base.component.zcomponent import BaseComponent
from galang_utils.rigbuilder.modules.module_limb.component.fk import LimbFKComponent
from galang_utils.rigbuilder.modules.module_limb.component.ik import LimbIKComponent
from galang_utils.rigbuilder.modules.module_limb.component.result import LimbResultComponent
from galang_utils.rigbuilder.modules.module_limb.component.settings import LimbSettingComponent
from galang_utils.rigbuilder.modules.module_limb.component.grp import LimbGroupComponent


class LimbComponent(BaseComponent):
    def __init__(self, module: ModuleInfo):
        super().__init__(module)
        self.module = module

        self.fk = LimbFKComponent(module)
        self.ik = LimbIKComponent(module)
        self.result = LimbResultComponent(module)
        self.setting = LimbSettingComponent(module)
        self.group = LimbGroupComponent(module)
        self.bind_connection: Dict = {}

    def create_bind(self):
        self.bind.create()

    def create_component(self):
        self.group.create()
        self.fk.create()
        self.ik.create()
        self.result.create()
        self.setting.create()

        # Add result joints to bind connection
        for guide, data in self.result.map.items():
            self.bind_connection[guide] = data[JNT]
