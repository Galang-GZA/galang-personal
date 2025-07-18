from maya import cmds
from typing import Dict, List
from galang_utils.rigbuilder.constant.project import role as P_ROLE
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupCreator
from galang_utils.rigbuilder.modules.limb.program.control import LimbControlCreator
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
        fk_grp_types = [P_ROLE.TOP]
        fk_grp = LimbGroupCreator(fk_grp_types, self.module)
        fk_grp.create()
        self.groups = fk_grp.map

        fk_grp_top = self.groups.get(P_ROLE.TOP)

        # step 1: Create FK joint chain
        fk_jnt = LimbJointChainSetup(self.guide.name, P_ROLE.FK)
        fk_jnt.create()
        self.groups[P_ROLE.JNT] = fk_jnt.group
        self.joints = fk_jnt.output

        # Step 2: Create FK controls
        parent_entry = None
        for guide in self.module.guides:
            cmds.select(clear=True)
            fk_manipulator = LimbControlCreator(guide, P_ROLE.FK, self.module)
            fk_manipulator.create()
            self.controls.append(fk_manipulator)

            if not parent_entry:
                cmds.parent(fk_manipulator.top, fk_grp_top)
            else:
                cmds.parent(fk_manipulator.top, parent_entry)
            parent_entry = fk_manipulator.ctrl