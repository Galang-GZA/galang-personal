from typing import List

from rigbuilder.modules.base.operator.dg import Node
from rigbuilder.modules.base.operator.setup_bind import BindOperator
from rigbuilder.modules.base.operator.setup_fk import FKOperator


class Operator:
    def __init__(self, guide):
        self.bind = BindOperator(guide)
        self.fk = FKOperator(guide)

    def run(self):
        operators: List[Node] = [self.bind, self.fk]
        for operator in operators:
            operator.run()
