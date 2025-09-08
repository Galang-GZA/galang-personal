from typing import List
from maya import cmds

from galang_utils.rigbuilder.constants.project import role as role
from galang_utils.rigbuilder.cores.guide import ModuleInfo
from galang_utils.rigbuilder.modules.base.component.group import GroupNode


class GroupComponent:
    def __init__(self, module: ModuleInfo):
        guide = module.guide
        self.rig = GroupNode(guide, module, [role.RIG, role.GROUP])
        self.dnt = GroupNode(guide, module, [role.DNT, role.GROUP])
        self.constraint = GroupNode(guide, module, [role.CONSTRAINT, role.BUFFER])

    def create(self):
        # STEP 0 : CREATE PRE COMPUTED COMPONENTS
        groups: List[GroupNode] = [self.rig, self.dnt, self.constraint]
        for group in groups:
            group.create()

        # STEP 1 : PARENT CONSTRAINT BUFFER TO DNT
        cmds.parent(self.constraint, self.dnt)
