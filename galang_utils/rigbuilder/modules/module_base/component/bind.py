from typing import Dict
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.module_base.rule.constant_module import *
from galang_utils.rigbuilder.modules.module_base.program.jointchain import LimbJointChainSetup


class BaseBindComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.map: Dict = {}

    def create(self):
        # Step 1 : Create bind joint chain
        ik_joint_chain = LimbJointChainSetup(self.guide.name, None, False)
        ik_joint_chain.build()

        # Step 2 : Map bind joints
        self.map = ik_joint_chain.output
