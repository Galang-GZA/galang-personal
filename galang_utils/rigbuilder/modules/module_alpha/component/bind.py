from typing import Dict
from galang_utils.rigbuilder.guides.guide import ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.constant.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.base.jointchain import LimbJointChainSetup


class LimbBindComponent:
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
