from typing import Dict, List
from rigbuilder.core.guide import ModuleInfo
from rigbuilder.modules.base.component.joint_chain import JointChain


class BindComponent:
    def __init__(self, module: ModuleInfo):
        self.guide = module.guide
        self.joints = JointChain(self.guide.name, create_group=False)

    def create(self):
        # Step 0 : Create bind joint chain
        self.joints.create()
