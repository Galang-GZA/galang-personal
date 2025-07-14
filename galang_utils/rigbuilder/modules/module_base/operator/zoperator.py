from galang_utils.rigbuilder.modules.module_base.operator.bind import BaseBindOperator
from galang_utils.rigbuilder.modules.module_base.operator.rig import BaseRigOperator


class BaseOperator:
    def __init__(self, guide):
        self._bind = BaseBindOperator(guide)
        self.rig = BaseRigOperator(guide)

    def run_bind(self):
        self._bind.run()

    def run(self):
        for name, attr in vars(self).items():
            if not name.startswith("_"):
                attr.run()
