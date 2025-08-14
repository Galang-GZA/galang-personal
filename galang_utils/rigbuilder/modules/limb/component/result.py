from maya import cmds

from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.core.guide import ModuleInfo

from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat
from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupNode
from galang_utils.rigbuilder.modules.limb.program.jointchain import LimbJointSet


class LimbResultComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.guides = module.guides
        self.group = LimbGroupNode(self.guide, module, role.RESULT, [role.RIG, role.GROUP])
        self.joints = LimbJointSet(module, role.RESULT)

        format = LimbFormat(self.guide.side, role.RESULT)
        self.pair_blends = [(format.name(guide.name_raw, role.PAIRBLEND), guide) for guide in self.guides]
        self.scale_blends = [(format.name(guide.name_raw, role.SCALEBLEND), guide) for guide in self.guides]

    def create(self):
        # Step 0: Create result components
        self.group.create()
        self.joints.create()

        # Step 1 : Create connection nodes
        for pair_blend, scale_blend in zip(self.pair_blends, self.scale_blends):
            cmds.createNode("pairBlend", name=pair_blend)
            cmds.createNode("blendColors", name=scale_blend)
