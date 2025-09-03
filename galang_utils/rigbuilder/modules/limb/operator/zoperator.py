from typing import List
from galang_utils.rigbuilder.modules.base.operator.zoperator import Operator

from rigbuilder.modules.base.operator.dg import Node
from rigbuilder.modules.base.operator.zoperator import Operator
from rigbuilder.modules.limb.component.zcomponent import LimbComponent
from rigbuilder.modules.limb.operator.setup_ik import LimbIKOperator
from rigbuilder.modules.limb.operator.setup_result import LimbResultOperator
from rigbuilder.modules.limb.operator.setup_detail import LimbDetailOperator
from rigbuilder.modules.limb.operator.setup_settings import LimbSettingOperator
from rigbuilder.modules.limb.operator.setup_group import LimbGroupOperator


class LimbOperator(Operator):
    def __init__(self, component: LimbComponent):
        super().__init__(Operator)

        self.bind_detail = None
        self.ik = LimbIKOperator(component)
        self.result = LimbResultOperator(component)
        self.detail = LimbDetailOperator(component)
        self.setting = LimbSettingOperator(component)
        self.group = LimbGroupOperator(component)

    def run(self):
        operators: List[Node] = [
            self.bind,
            self.bind_detail,
            self.fk,
            self.ik,
            self.result,
            self.detail,
            self.setting,
            self.group,
        ]
        for operator in operators:
            operator.run()
