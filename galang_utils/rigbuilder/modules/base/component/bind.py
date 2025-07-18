from typing import Dict, List
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.base.program.jointchain import BaseJointChainSetup


class BaseBindComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.joints: List = {}
        

    def create(self):
        # Step 1 : Create bind joint chain
        bind_joint_chain = BaseJointChainSetup(self.guide.name, create_group=False)
        bind_joint_chain.create()
        self.joints = bind_joint_chain.joints
