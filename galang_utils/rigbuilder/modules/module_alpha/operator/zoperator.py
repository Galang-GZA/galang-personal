from galang_utils.rigbuilder.modules.module_limb.operator.bind import LimbBindOperator
from galang_utils.rigbuilder.modules.module_limb.operator.fk import LimbFKOperator
from galang_utils.rigbuilder.modules.module_limb.operator.ik import LimbIKOperator
from galang_utils.rigbuilder.modules.module_limb.operator.result import LimbResultOperator
from galang_utils.rigbuilder.modules.module_limb.operator.settings import LimbSettingOperator


class LimbOperator:
    def __init__(self, guide):
        self.bind = LimbBindOperator(guide)
        self.fk = LimbFKOperator(guide)
        self.ik = LimbIKOperator(guide)
        self.result = LimbResultOperator(guide)
        self.setting = LimbSettingOperator(guide)

    def run_bind(self):
        self.bind.run()

    def run_fk(self):
        self.fk.run()

    def run_ik(self):
        self.ik.run()

    def run_result(self):
        self.result.run()

    def run_setting(self):
        self.setting.run()
