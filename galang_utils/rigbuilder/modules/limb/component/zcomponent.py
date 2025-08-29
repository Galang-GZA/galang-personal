from typing import List

from galang_utils.rigbuilder.core.guide import ModuleInfo

from rigbuilder.modules.base.component.z_component import BaseComponent
from galang_utils.rigbuilder.modules.limb.component.fk import LimbFKComponent
from galang_utils.rigbuilder.modules.limb.component.ik import LimbIKComponent
from galang_utils.rigbuilder.modules.limb.component.result import LimbResultComponent
from rigbuilder.modules.limb.component.twist import LimbRollComponent
from galang_utils.rigbuilder.modules.limb.component.settings import LimbSettingComponent
from rigbuilder.modules.limb.component.group import LimbContainerComponent


class LimbComponent(BaseComponent):
    def __init__(self, module: ModuleInfo):
        super().__init__(module)
        self.module = module

        self.fk = LimbFKComponent(module)
        self.ik = LimbIKComponent(module)
        self.result = LimbResultComponent(module)
        self.setting = LimbSettingComponent(module)
        self.sub = LimbRollComponent(module)
        self.container = LimbContainerComponent(module)

    def bind_twist(self):
        pass

    def create_rig(self):
        self.container.create()
        self.fk.create()
        self.ik.create()
        self.result.create()
        self.sub.create()
        self.setting.create()

        # Add result joints to bind connection
        self.bind_connection = self.result.joints
