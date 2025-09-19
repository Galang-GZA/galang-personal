from typing import List
from galang_utils.rig_x_frame.mod_zero.base.operator.zoperator import Operator

from rig_x_frame.mod_zero.base.operator.dg import Node
from rig_x_frame.mod_zero.base.operator.zoperator import Operator
from rig_x_frame.mod_zero.limb.component.zcomponents import LimbComponents
from rig_x_frame.mod_zero.limb.operator.setup_ik import LimbIKOperator
from rig_x_frame.mod_zero.limb.operator.setup_result import LimbResultOperator
from rig_x_frame.mod_zero.limb.operator.setup_detail import LimbDetailOperator
from rig_x_frame.mod_zero.limb.operator.setup_settings import LimbSettingOperator
from rig_x_frame.mod_zero.limb.operator.setup_group import LimbGroupOperator


class LimbOperator(Operator):
    def __init__(self, component: LimbComponents):
        super().__init__(Operator)

        self.ik = LimbIKOperator(component)
        self.result = LimbResultOperator(component)
        self.detail = LimbDetailOperator(component)
        self.setting = LimbSettingOperator(component)
        self.group = LimbGroupOperator(component)

    def run(self):
        operators: List[Node] = [
            self.bind,
            self.fk,
            self.ik,
            self.setting,
            self.result,
            self.detail,
            self.group,
        ]
        for operator in operators:
            operator.run()
