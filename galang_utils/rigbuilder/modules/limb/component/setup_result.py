from maya import cmds
from typing import List
from galang_utils.rigbuilder.constants.project import role as role
from galang_utils.rigbuilder.cores.guide import ModuleInfo
from rigbuilder.modules.base.component.dag import Node

from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat
from galang_utils.rigbuilder.modules.base.component.group import GroupNode
from rigbuilder.modules.base.component.joint_chain import JointChain


class LimbResultComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.guides = module.guides
        self.group = GroupNode(self.guide, module, role.RESULT, [role.RIG, role.GROUP])
        self.joints = JointChain(self.guides, module, role.RESULT)

        """ MASUKIN YANG DG DG DI OPERATOR"""
        # format = LimbFormat(self.guide.side, role.RESULT)
        # self.pair_blends = [(format.name(guide.name_raw, role.PAIRBLEND), guide) for guide in self.guides]
        # self.scale_blends = [(format.name(guide.name_raw, role.SCALEBLEND), guide) for guide in self.guides]

    def create(self):
        # Step 0: Create result components
        components: List[Node] = [self.group, self.joints]
        for component in components:
            component.create()

        # Step 1 : Create connection nodes
        """ MASUKIN YANG DG DG DI OPERATOR"""
        # for pair_blend, scale_blend in zip(self.pair_blends, self.scale_blends):
        #     cmds.createNode("pairBlend", name=pair_blend)
        #     cmds.createNode("blendColors", name=scale_blend)
