from galang_utils.rigbuilder.modules.base.operator.zoperator import BaseOperator

from galang_utils.rigbuilder.modules.limb.component.zcomponent import LimbComponent
from galang_utils.rigbuilder.modules.limb.operator.fk import LimbFKOperator
from galang_utils.rigbuilder.modules.limb.operator.ik import LimbIKOperator
from galang_utils.rigbuilder.modules.limb.operator.result import LimbResultOperator
from rigbuilder.modules.limb.operator.sub import LimbRollOperator
from galang_utils.rigbuilder.modules.limb.operator.settings import LimbSettingOperator
from galang_utils.rigbuilder.modules.limb.operator.grp import LimbGroupOperator


class LimbOperator(BaseOperator):
    def __init__(self, component: LimbComponent):
        super().__init__(component)

        self.fk = LimbFKOperator(component)
        self.ik = LimbIKOperator(component)
        self.result = LimbResultOperator(component)
        self.roll = LimbRollOperator(component)
        self.setting = LimbSettingOperator(component)
        self.group = LimbGroupOperator(component)
