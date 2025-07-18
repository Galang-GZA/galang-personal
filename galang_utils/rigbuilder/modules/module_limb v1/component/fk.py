from maya import cmds
from typing import Dict, List
from galang_utils.rigbuilder.constant.project import role as P_ROLE
from galang_utils.rigbuilder.core.guide import ModuleInfo

from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat 
from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupCreator

from rigbuilder.modules.limb.program.control import LimbControlCreator
from galang_utils.rigbuilder.modules.limb.program.jointchain import LimbJointChainSetup



class LimbFKComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.groups: Dict = {}
        self.joints: List = []
        self.controls: List[LimbControlCreator] = []

    def create(self):
        # Step 0: Create FK module goup
        fk_grp_types = [P_ROLE.GROUP]
        fk_grp = LimbGroupCreator(fk_grp_types, self.module)
        fk_grp.create()
        self.groups = fk_grp.map

        fk_grp_top = self.groups.get(P_ROLE.GROUP)

        # step 1: Create FK joint chain
        fk_jnt_chain = LimbJointChainSetup(self.guide.name, P_ROLE.FK)
        fk_jnt_chain.create()
        self.groups[P_ROLE.JNT] = fk_jnt_chain.group
        cmds.parent(self.groups[P_ROLE.JNT], fk_grp_top)

        # Step 2: Create FK controls
        parent_entry = None
        for guide_jnt in self.module.guides + self.module.guides_end:
            cmds.select(clear=True)
            fk_manipulator = LimbControlCreator(guide_jnt, P_ROLE.FK, self.module)
            fk_manipulator.create()

            if not parent_entry:
                cmds.parent(fk_manipulator.top, self.groups[P_ROLE.MAIN])
            else:
                cmds.parent(fk_manipulator.top, parent_entry)
            parent_entry = fk_manipulator.ctrl

            # Step 3 : Map FK controls and joints
            fk_joint = fk_jnt_chain.output.get(guide_jnt.name)
            self.joints.append(fk_joint)
            self.controls.append(fk_manipulator)
