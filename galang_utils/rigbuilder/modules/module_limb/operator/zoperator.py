from galang_utils.rigbuilder.modules.module_base.operator.zoperator import BaseOperator

from galang_utils.rigbuilder.modules.module_limb.component.zcomponent import LimbComponent
from galang_utils.rigbuilder.modules.module_limb.operator.fk import LimbFKOperator
from galang_utils.rigbuilder.modules.module_limb.operator.ik import LimbIKOperator
from galang_utils.rigbuilder.modules.module_limb.operator.result import LimbResultOperator
from galang_utils.rigbuilder.modules.module_limb.operator.settings import LimbSettingOperator


class LimbOperator(BaseOperator):
    def __init__(self, component: LimbComponent):
        super().__init__(component)

        self.fk = LimbFKOperator(component)
        self.ik = LimbIKOperator(component)
        self.result = LimbResultOperator(component)
        self.setting = LimbSettingOperator(component)

    def run_bind(self):
        self.bind.run()

    def run_component(self):
        self.fk.run()
        self.ik.run()
        self.result.run()
        self.setting.run()
