from maya import cmds
from typing import Dict, Union, List
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.rule.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.program.controls import LimbControlCreator
from galang_utils.rigbuilder.modules.module_limb.program.jointchain import LimbJointChainSetup


class LimbFKComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.map: Dict[GuideInfo, Dict[str, Union[LimbControlCreator, str]]] = {}
        self.groups: Dict = {}
        self.joints: List = []
        self.controls: List = []

    def create(self):
        # Step 0: Create FK module goup
        group_name = limb_level_format(PROJECT, FK, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.groups[MASTER] = cmds.group(em=True, name=group_name)
            cmds.xform(self.groups[MASTER], t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # step 1: Create FK joint chain
        fk_joint_chain = LimbJointChainSetup(self.guide.name, FK)
        fk_joint_chain.build()
        self.groups[JNT] = fk_joint_chain.group

        # Step 2: Create FK controls
        parent_entry = None
        for guide_jnt in self.module.guides + self.module.guides_end:
            cmds.select(clear=True)
            fk_control = LimbControlCreator(guide_jnt, FK, self.module)
            fk_control.create()

            if not parent_entry:
                cmds.parent(fk_control.top, self.groups[MASTER])
            else:
                cmds.parent(fk_control.top, parent_entry)
            parent_entry = fk_control.ctrl

            # Step 3 : Map FK controls and joints
            fk_joint = fk_joint_chain.output.get(guide_jnt.name)
            self.map[guide_jnt.name] = {CTRL: fk_control, JNT: fk_joint}
            self.joints.append(fk_joint)
            self.controls.append(fk_control)
