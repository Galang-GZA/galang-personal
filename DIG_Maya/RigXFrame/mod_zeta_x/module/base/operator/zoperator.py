from typing import List

from rig_x_frame.mod_zero.base.operator.dg import Node
from rig_x_frame.mod_zero.base.operator.setup_bind import BindOperator
from rig_x_frame.mod_zero.base.operator.setup_fk import FKOperator


class Operator:
    def __init__(self, guide):
        self.bind = BindOperator(guide)
        self.fk = FKOperator(guide)

    def run(self):
        operators: List[Node] = [self.bind, self.fk]
        for operator in operators:
            operator.run()
