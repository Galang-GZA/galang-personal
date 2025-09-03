from maya import cmds
from typing import List
from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup
from rigbuilder.cores.guide import GuideInfo, ModuleInfo
from rigbuilder.modules.base.component.dag import Node
from rigbuilder.modules.base.component.group import GroupNode


class LocatorNode(Node):
    """
    LimbLocatorNode behaves like a string (the Maya node name) but also carries extra
    metadata (position, orientation, etc.) and has helper methods like create().
    """

    def __init__(
        self,
        guide: GuideInfo,
        module: ModuleInfo,
        types: List = None,
        position: List[float] = None,
    ):
        # pre-compute locator name
        locator_types = types.append(role.LOCATOR)
        super().__init__(guide, module, locator_types, position)

    def create(self):
        """
        Creates an empty Maya group at the given position & orientation.
        """
        loc_node = cmds.spaceLocator(name=self)
        cmds.xform(loc_node, t=self.position, ro=self.orientation)


class LimbLocatorSet(List[LocatorNode]):
    """
    A collection of LimbLocatorSet indexed by their locator index and type (e.g. "STRETCH", "BASE", "BLEND", etc.).
    """

    def __init__(
        self,
        guides,
        module: ModuleInfo,
        kinematics: str,
        types: List,
        positions: List = None,
    ):
        super().__init__()
        self.group = GroupNode(guide, module, kinematics, [role.LOCATOR, role.GROUP])

        # Pre-compute locators (they’re not yet in Maya)
        # Pre-compute general locators
        pv_pos = module.guides_pv.position
        for i, (guide, position) in enumerate(zip(guides, positions)):
            i = f"{i+1:02d}"
            resolved_types = [(i if t is setup.INDEX else t) for t in types]
            resolved_position = pv_pos if role.ACTIVE in types and i == 1 else position
            locator_node = LocatorNode(guide, module, resolved_types, resolved_position)
            self.append(locator_node)

    def create(self):
        # Create group node
        self.group.create()

        # Create guide positioned locators
        for loc in self:
            loc.create()
