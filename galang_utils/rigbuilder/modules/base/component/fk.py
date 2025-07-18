from maya import cmds
from typing import Dict, List
from galang_utils.rigbuilder.constant.project import role as P_ROLE
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.base.program.group import BaseGroupCreator
from galang_utils.rigbuilder.modules.base.program.control import BaseControlCreator
from galang_utils.rigbuilder.modules.base.program.jointchain import BaseJointChainSetup


class BaseFKComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.guides = module.guides
        self.groups: Dict = {}
        self.joints: List = []
        self.controls: List [BaseControlCreator] = []

    def create(self):
        # Step 0: Create FK module goup
        fk_grp_types = [P_ROLE.MASTER]
        fk_grp = BaseGroupCreator(fk_grp_types, self.module)
        fk_grp.create()
        self.groups = fk_grp.map
        fk_grp_top = self.groups.get(P_ROLE.MASTER)

        # step 1: Create FK joint chain
        fk_chain = BaseJointChainSetup(self.guide.name, P_ROLE.FK, create_group=False)
        fk_chain.create()
        fk_chain.joints = self.joints

        # Step 2: Create FK controls and parent the joints
        parent_entry = None
        for guide_jnt, fk_jnt in zip (self.guides, self.joints):
            cmds.select(clear=True)
            fk_manipulator = BaseControlCreator(guide_jnt, P_ROLE.FK, self.module)
            fk_manipulator.create()
            self.controls.append(fk_manipulator)

            # Setup fk control hierarchy
            if not parent_entry:
                cmds.parent(fk_manipulator.top, fk_grp_top)
            else:
                cmds.parent(fk_manipulator.top, parent_entry)
            parent_entry = fk_manipulator.ctrl

            # Parent FK joints to its controls
            cmds.parent(fk_jnt, fk_manipulator.ctrl)
            
