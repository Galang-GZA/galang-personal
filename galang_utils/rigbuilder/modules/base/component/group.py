from maya import cmds
from typing import Dict, List
from rigbuilder.constant.project import role as role
from rigbuilder.modules.limb.constant.format import LimbFormat
from rigbuilder.core.guide import GuideInfo, ModuleInfo
from rigbuilder.modules.base.component.dag import Node


class GroupNode(Node):
    """
    LimbGroupNode behaves like a string (the Maya node name) but also carries extra
    metadata (position, orientation, etc.) and has helper methods like create().
    """

    def __init__(
        self,
        guide: GuideInfo,
        module: ModuleInfo,
        types: List = [],
        position: List[float] = None,
    ):
        super().__init__(guide, module, types, position)

    def create(self):
        """
        Creates an empty Maya group at the given position & orientation.
        """
        grp_node = cmds.group(em=True, name=self)
        cmds.xform(grp_node, t=self.position, ro=self.orientation)
