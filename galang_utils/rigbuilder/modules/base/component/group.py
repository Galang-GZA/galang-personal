from maya import cmds
from typing import Dict, List
from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat
from galang_utils.rigbuilder.core.guide import GuideInfo, ModuleInfo
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
        orientation: List[float] = None,
    ):
        super().__init__(guide, module, types, position, orientation)

    def create(self):
        """
        Creates an empty Maya group at the given position & orientation.
        """
        grp_node = cmds.group(em=True, name=self)
        cmds.xform(grp_node, t=self.position, ro=self.orientation)
