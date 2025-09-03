from typing import List
from galang_utils.rigbuilder.constants.project import role as role
from galang_utils.rigbuilder.cores.guide import ModuleInfo
from galang_utils.rigbuilder.modules.base.component.group import GroupNode


class LimbGroupComponent:
    def __init__(self, module: ModuleInfo):
        guide = module.guide
        self.rig = GroupNode(guide, module, [role.RIG, role.GROUP])
        self.dnt = GroupNode(guide, module, [role.DNT, role.GROUP])
        self.constraint = GroupNode(guide, module, [role.CONSTRAINT, role.GROUP])

    def create(self):
        groups: List[GroupNode] = [self.rig, self.dnt, self.constraint]
        for group in groups:
            group.create()
