from galang_utils.rigbuilder.modules.module_limb.component.bind import LimbBindComponent
from galang_utils.rigbuilder.modules.module_limb.component.fk import LimbFKComponent
from galang_utils.rigbuilder.modules.module_limb.component.ik import LimbIKComponent
from galang_utils.rigbuilder.modules.module_limb.component.result import LimbResultComponent
from galang_utils.rigbuilder.modules.module_limb.component.settings import LimbSettingComponent


class LimbComponent:
    def __init__(self, guide):
        self.bind = LimbBindComponent(guide)
        self.fk = LimbFKComponent(guide)
        self.ik = LimbIKComponent(guide)
        self.result = LimbResultComponent(guide)
        self.setting = LimbSettingComponent(guide)

    def create_bind(self):
        self.bind.create()

    def create_fk(self):
        self.fk.create()

    def create_ik(self):
        self.ik.create()

    def create_result(self):
        self.result.create()

    def create_setting(self):
        self.setting.create()
