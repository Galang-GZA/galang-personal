from typing import Dict
from galang_utils.rigbuilder.constant.constant_project import *
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.base.component.zcomponent import BaseComponent
from galang_utils.rigbuilder.modules.limb.component.fk import LimbFKComponent
from galang_utils.rigbuilder.modules.limb.component.ik import LimbIKComponent
from galang_utils.rigbuilder.modules.limb.component.result import LimbResultComponent
from rigbuilder.modules.limb.component.sub import LimbRollComponent
from galang_utils.rigbuilder.modules.limb.component.settings import LimbSettingComponent
from rigbuilder.modules.limb.component.container import LimbGroupComponent


class LimbComponent(BaseComponent):
    def __init__(self, module: ModuleInfo):
        super().__init__(module)
        self.module = module

        self.fk = LimbFKComponent(module)
        self.ik = LimbIKComponent(module)
        self.result = LimbResultComponent(module)
        self.setting = LimbSettingComponent(module)
        self.roll = LimbRollComponent(module)
        self.group = LimbGroupComponent(module)
        self.bind_connection: Dict = {}

    def create_rig(self):
        self.group.create()
        self.fk.create()
        self.ik.create()
        self.result.create()
        self.roll.create()
        self.setting.create()

        # Add result joints to bind connection
        for guide, data in self.result.map.items():
            self.bind_connection[guide] = data[JNT]
