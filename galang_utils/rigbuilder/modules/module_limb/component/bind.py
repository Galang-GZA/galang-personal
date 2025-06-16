from maya import cmds
from typing import Dict
from galang_utils.curve.shapes_library import *
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.guides.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.constant.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.base.jointchain import LimbJointChainSetup


class LimbBindComponent:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.map: Dict = {}

    def create(self):
        # Step 1 : Create bind joint chain
        ik_joint_chain = LimbJointChainSetup(self.guide.name)
        ik_joint_chain.build()

        # Step 2 : Map bind joints
        self.bind_limb_map = ik_joint_chain.output
