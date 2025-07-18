from maya import cmds
from typing import Dict, List

from galang_utils.rigbuilder.constant.project import role as TASK_ROLE

from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat 
from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupCreator
from galang_utils.rigbuilder.modules.limb.program.jointchain import LimbJointChainSetup


class LimbResultComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.joints: List = []
        self.pair_blends: List = []
        self.scale_blends: List = []
        self.groups: Dict = {}
        self.format = LimbFormat(self.guide.side, TASK_ROLE.RESULT)

    def create(self):
        # Step 0: Create result Module Group
        result_grp_types = [TASK_ROLE.RESULT]
        result_grp = LimbGroupCreator(result_grp_types, self.module)
        result_grp.create()
        self.groups = result_grp.map

        result_grp_top = self.groups.get(TASK_ROLE.RESULT)

        # Step 1 : Create result joint chain
        result_jnt_chain = LimbJointChainSetup(self.guide.name, TASK_ROLE.RESULT)
        result_jnt_chain.create()
        cmds.parent(result_jnt_chain.group, result_grp_top)
        self.groups[TASK_ROLE.JNT] = result_jnt_chain.output

        # Step 2 : Create connection nodes
        for index, guide in enumerate(self.module.guides):
            result_joint = self.joints[index]
            pairblend_name = self.format(guide.name_raw, TASK_ROLE.PAIRBLEND)
            blendcolor_name = self.format(guide.name_raw, TASK_ROLE.SCALEBLEND)
            pair_blend = cmds.createNode("pairBlend", name=pairblend_name)
            scale_blend = cmds.createNode("blendColors", name=blendcolor_name)

            # Step 3 : Map result joints and connection nodes
            self.nodes[guide.name] = { TASK_ROLE.PAIRBLEND: pair_blend, TASK_ROLE.SCALEBLEND: scale_blend}
