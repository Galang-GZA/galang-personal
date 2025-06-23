from maya import cmds
from typing import Dict, Union
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.module_base.rule.constant_module import *
from galang_utils.rigbuilder.modules.module_base.program.controls import BaseControlCreator
from galang_utils.rigbuilder.modules.module_base.program.jointchain import BaseJointChainSetup


class BaseRigComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.map: Dict[GuideInfo, Dict[str, Union[BaseControlCreator, str]]] = {}
        self.group: str = None

    def create(self):
        # Step 0: Create FK module goup
        group_name = base_level_format(PJ, FK, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.group = cmds.group(em=True, name=group_name)
            cmds.xform(self.group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # step 1: Create FK joint chain
        fk_joint_chain = BaseJointChainSetup(self.guide.name, FK)
        fk_joint_chain.build()
        cmds.parent(fk_joint_chain.group, self.group)

        # Step 2: Create FK controls
        parent_entry = None
        for guide_jnt in self.module.guides + self.module.guides_end:
            cmds.select(clear=True)
            fk_control = BaseControlCreator(guide_jnt, FK, self.module)
            fk_control.create()

            if not parent_entry:
                cmds.parent(fk_control.top, self.group)
            else:
                cmds.parent(fk_control.top, parent_entry)
            parent_entry = fk_control.ctrl

            # Step 3 : Map FK controls and joints
            fk_joint = fk_joint_chain.output.get(guide_jnt.name)
            self.map[guide_jnt.name] = {CTRL: fk_control, JNT: fk_joint}
