from maya import cmds
from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupNode
from galang_utils.rigbuilder.modules.limb.program.control import LimbControlSet
from galang_utils.rigbuilder.modules.limb.program.jointchain import LimbJointSet


class LimbFKComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.guides = module.guides
        self.group = LimbGroupNode(self.guide, module, role.FK, [role.RIG, role.GROUP])
        self.joints = LimbJointSet(self.guides, module, role.FK)
        self.controls = LimbControlSet(self.guides, module, role.FK)

    def create(self):
        # Step 0: Create FK components
        self.group.create()
        self.joints.create()
        self.controls.create()
