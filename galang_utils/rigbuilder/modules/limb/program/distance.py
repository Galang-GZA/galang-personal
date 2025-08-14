from maya import cmds
from typing import List
from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.limb.program.base import LimbBaseNode
from galang_utils.rigbuilder.modules.limb.program.group import LimbGroupNode


class LimbDistanceNode(LimbBaseNode):
    """
    LimbDistanceNode behaves like a string (the Maya node name) but also carries
    helper methods like create().
    """

    def __init__(
        self,
        guide: GuideInfo,
        module: ModuleInfo,
        kinematics: str,
        node_type: str = None,
        sub_type1: str = None,
        sub_type2: str = None,
        index: int = None,
        position: List[float] = None,
        orientation: List[float] = None,
    ):
        super().__init__(guide, module, kinematics, node_type, sub_type1, sub_type2, index, position, orientation)

    def create(self):
        """
        Creates an empty Maya distance node.
        """
        cmds.rename(cmds.createNode("distanceDimShape"), f"{self}_shape")
        cmds.rename("distanceDimension1", self)


class LimbDistanceSet(List[LimbDistanceNode]):
    """
    A list of LimbDistanceNode indexed by their locator index and type (e.g. "STRETCH", "BASE", "BLEND", etc.).
    """

    def __init__(self, module: ModuleInfo, kinematics: str, sub_type1, sub_types2: List):
        super().__init__()
        guide = module.guide
        guides = module.guides
        self.sub_type1 = sub_type1
        self.sub_types2 = sub_types2
        self.group = LimbGroupNode(guide, module, kinematics, role.DISTANCE, sub_type1, level=role.GROUP)

        # Pre-computes guide locator (they’re not yet in Maya)
        for guide in guides:
            distance_node = LimbDistanceNode(guide, module, kinematics, role.DISTANCE, sub_type1)
            self.append(distance_node)

        # Pre-compute soft IK locators
        if sub_type1 == role.ACTIVE:
            self.stretch = LimbDistanceNode(guides[2], module, kinematics, role.DISTANCE, sub_type1, role.STRETCH)
            self.base = LimbDistanceNode(guides[2], module, kinematics, role.DISTANCE, sub_type1, role.BASE)
            self.blend = LimbDistanceNode(guides[2], module, kinematics, role.DISTANCE, sub_type1, role.BLEND)
            self.list: List[LimbDistanceNode] = [self.stretch, self.base, self.blend]

    def create(self):
        # Create guide positioned locators
        for dis in self:
            dis.create()

        # Create soft IK locators
        for extra_dis in self.list:
            extra_dis.create()
