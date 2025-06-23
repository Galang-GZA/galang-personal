from galang_utils.rigbuilder.modules.module_base.operator.bind import BaseBindOperator
from galang_utils.rigbuilder.modules.module_base.operator.rig import BaseRigOperator


class BaseOperator:
    def __init__(self, guide):
        self.bind = BaseBindOperator(guide)
        self.fk = BaseRigOperator(guide)

    def run_bind(self):
        self.bind.run()

    def run_fk(self):
        self.fk.run()
