from maya import cmds
from typing import List
from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup
from rigbuilder.modules.base.component.dag import Node


class LocatorNode(Node):
    """
    LimbLocatorNode behaves like a string (the Maya node name) but also carries extra
    metadata (position, orientation, etc.) and has helper methods like create().
    """

    def __init__(self, guide_name, side, types: List, position: List[float], orientation: List[float]):
        # pre-compute locator name
        locator_types = types + [role.LOCATOR]
        super().__init__(guide_name, side, locator_types, position, orientation)

    def create(self):
        """
        Creates an empty Maya group at the given position & orientation.
        """
        loc_node = cmds.spaceLocator(name=self)
        cmds.xform(loc_node, t=self.position, ro=self.orientation)


class LocatorSet(List[LocatorNode]):
    """
    A collection of LimbLocatorSet indexed by their locator index and type.
    """

    def __init__(self, guide_names: List, side: str, types: List, positions: List[float], orientations: List[float]):
        super().__init__()
        group_types = types + [role.GROUP]
        self.group = Node(guide_names[0], side, group_types, positions[0], orientations[0])

        # Pre-compute locators
        for i, (guide_name, position, orientation) in enumerate(zip(guide_names, positions, orientations)):
            i = f"{i+1:02d}"
            resolved_types = [(i if type is setup.INDEX else type) for type in types]
            locator_node = LocatorNode(guide_name, side, resolved_types, position, orientation)
            self.append(locator_node)

    def create(self):
        # Create group node
        self.group.create()

        # Create guide positioned locators
        for loc in self:
            loc.create()
