from maya import cmds
from typing import List
from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo
from rigbuilder.modules.base.component.dag import Node
from galang_utils.rigbuilder.modules.base.component.group import GroupNode


class DistanceNode(Node):
    """
    LimbDistanceNode behaves like a string (the Maya node name) but also carries
    helper methods like create().
    """

    def __init__(
        self,
        guide: GuideInfo,
        module: ModuleInfo,
        types: List = None,
        position: List[float] = None,
        orientation: List[float] = None,
    ):
        distance_types = types.append(role.DISTANCE)
        super().__init__(guide, module, types, distance_types, position, orientation)

    def create(self):
        """Creates an empty Maya distance node."""
        cmds.rename(cmds.createNode("distanceBetween"), self)


class DistanceSet(List[DistanceNode]):
    """A list of LimbDistanceNode indexed by their locator index and type (e.g. "STRETCH", "BASE", "BLEND", etc.)."""

    def __init__(self, guides, module: ModuleInfo, types: List):
        super().__init__()
        # Pre-computes guide locator (they’re not yet in Maya)
        for guide in guides:
            distance_node = DistanceNode(guide, module, types)
            self.append(distance_node)

    def create(self):
        # Create guide positioned locators
        for dis in self:
            dis.create()
