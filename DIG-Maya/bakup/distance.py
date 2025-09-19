from maya import cmds
from typing import List
from galang_utils.rig_x_frame.constants.project import role as role
from galang_utils.rig_x_frame.core.guide import GuideInfo, ModuleInfo
from rig_x_frame.mod_zero.base.component.dag import Node
from galang_utils.rig_x_frame.mod_zero.base.component.group import GroupNode


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
    ):
        types.append(role.DISTANCE)
        super().__init__(guide, module, types, types, position)

    def run(self):
        """Creates an empty Maya distance node."""
        cmds.rename(cmds.createNode("distanceBetween", n=self))


class DistanceSet(List[DistanceNode]):
    """A list of LimbDistanceNode indexed by their locator index and type (e.g. "STRETCH", "BASE", "BLEND", etc.)."""

    def __init__(self, guides, module: ModuleInfo, types: List):
        super().__init__()
        # Pre-computes guide locator (they’re not yet in Maya)
        for guide in guides:
            distance_node = DistanceNode(guide, module, types)
            self.append(distance_node)

    def run(self):
        # Create guide positioned locators
        for dis in self:
            dis.run()
