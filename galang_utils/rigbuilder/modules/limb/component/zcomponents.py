from typing import List

from galang_utils.rigbuilder.cores.guide import ModuleInfo

from rigbuilder.modules.base.component.dag import Node
from rigbuilder.modules.base.component.zcomponents import Components
from rigbuilder.modules.limb.component.setup_bind import LimbBindComponent
from rigbuilder.modules.limb.component.setup_ik import LimbIKComponent
from rigbuilder.modules.limb.component.setup_result import LimbResultComponent
from rigbuilder.modules.limb.component.setup_detail import LimbDetailComponent
from rigbuilder.modules.limb.component.setup_settings import LimbSettingComponent


class LimbComponents(Components):
    def __init__(self, module: ModuleInfo):
        super().__init__(module)
        self.bind = LimbBindComponent(module)
        self.ik = LimbIKComponent(module)
        self.result = LimbResultComponent(module)
        self.setting = LimbSettingComponent(module)
        self.detail = LimbDetailComponent(module)

    def create_rig(self):
        components: List[Node] = [self.fk, self.ik, self.result, self.setting, self.detail, self.group]
        for component in components:
            component.create()
