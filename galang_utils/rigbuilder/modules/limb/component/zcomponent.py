from typing import List

from galang_utils.rigbuilder.cores.guide import ModuleInfo

from rigbuilder.modules.base.component.dag import Node
from rigbuilder.modules.base.component.zcomponent import Component
from rigbuilder.modules.limb.component.setup_ik import LimbIKComponent
from rigbuilder.modules.limb.component.setup_result import LimbResultComponent
from rigbuilder.modules.limb.component.setup_detail import LimbDetailComponent
from rigbuilder.modules.limb.component.setup_settings import LimbSettingComponent
from rigbuilder.modules.limb.component.setup_group import LimbGroupComponent


class LimbComponent(Component):
    def __init__(self, module: ModuleInfo):
        super().__init__(module)
        self.bind_detail = None
        self.ik = LimbIKComponent(module)
        self.result = LimbResultComponent(module)
        self.setting = LimbSettingComponent(module)
        self.detail = LimbDetailComponent(module)
        self.group = LimbGroupComponent(module)
        self.bind_driver = self.result.joints
        self.bind_detail_driver = None

    def bind_twist(self):
        pass

    def create(self):
        components: List[Node] = [
            self.bind,
            self.bind_detail,
            self.fk,
            self.ik,
            self.result,
            self.setting,
            self.detail,
            self.group,
        ]
        for component in components:
            component.create()
