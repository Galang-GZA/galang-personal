from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupNode


class LimbGroupComponent:
    def __init__(self, module: ModuleInfo):
        guide = module.guide
        self.rig = LimbGroupNode(guide, module, [role.RIG, role.GROUP])
        self.dnt = LimbGroupNode(guide, module, [role.DNT, role.GROUP])
        self.constraint = LimbGroupNode(guide, module, [role.CONSTRAINT, role.GROUP])
        self.groups = [self.rig, self.dnt, self.constraint]

    def create(self):
        for group in self.groups:
            group.create()
