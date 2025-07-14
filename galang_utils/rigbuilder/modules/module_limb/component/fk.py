from maya import cmds
from typing import Dict, Union, List
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.rule.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.program.group import LimbGroupCreator
from galang_utils.rigbuilder.modules.module_limb.program.controls import LimbControlCreator
from galang_utils.rigbuilder.modules.module_limb.program.jointchain import LimbJointChainSetup


class LimbFKComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.groups: Dict = {}
        self.joints: List = []
        self.controls: List = []

    def create(self):
        # Step 0: Create FK module goup
        fk_grp_types = [GROUP]
        fk_grp = LimbGroupCreator(fk_grp_types, self.module)
        fk_grp.create()
        self.groups = fk_grp.map

        # step 1: Create FK joint chain
        fk_jnt = LimbJointChainSetup(self.guide.name, FK)
        fk_jnt.create()
        self.groups[JNT] = fk_jnt.group
        self.joints = fk_jnt.output

        # Step 2: Create FK controls
        parent_entry = None
        for g in self.module.guides + self.module.guides_end:
            cmds.select(clear=True)
            fk_ctrl = LimbControlCreator(g, FK, self.module)
            fk_ctrl.create()

            if not parent_entry:
                cmds.parent(fk_ctrl.top, self.groups[MASTER])
            else:
                cmds.parent(fk_ctrl.top, parent_entry)
            parent_entry = fk_ctrl.ctrl

            # Step 3 : Map FK controls and joints
            self.controls.append(fk_ctrl)
