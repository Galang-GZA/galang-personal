from galang_utils.rigbuilder.modules.module_base.operator.zoperator import BaseOperator
from galang_utils.rigbuilder.modules.module_limb.operator.fk import LimbFKOperator
from galang_utils.rigbuilder.modules.module_limb.operator.ik import LimbIKOperator
from galang_utils.rigbuilder.modules.module_limb.operator.result import LimbResultOperator
from galang_utils.rigbuilder.modules.module_limb.operator.settings import LimbSettingOperator


class LimbOperator(BaseOperator):
    def __init__(self, guide):
        super().__init__()

        self.fk = LimbFKOperator(guide)
        self.ik = LimbIKOperator(guide)
        self.result = LimbResultOperator(guide)
        self.setting = LimbSettingOperator(guide)

    def run_bind(self):
        self.bind.run()

    def run_component(self):
        self.fk.run()
        self.ik.run()
        self.result.run()
        self.setting.run()
