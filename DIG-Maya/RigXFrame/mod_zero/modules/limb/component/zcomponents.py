from typing import List

from galang_utils.rig_x_frame.core.guide import ModuleInfo

from rig_x_frame.mod_zero.base.component.dag import Node
from rig_x_frame.mod_zero.base.component.zcomponents import Components
from rig_x_frame.mod_zero.limb.component.setup_bind import LimbBindComponent
from rig_x_frame.mod_zero.limb.component.setup_ik import LimbIKComponent
from rig_x_frame.mod_zero.limb.component.setup_result import LimbResultComponent
from rig_x_frame.mod_zero.limb.component.setup_detail import LimbDetailComponent
from rig_x_frame.mod_zero.limb.component.setup_settings import LimbSettingComponent


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
