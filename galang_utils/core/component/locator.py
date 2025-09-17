from maya import cmds
from typing import List
from core.component.dag import Node
from core.constant.maya.dag import role as dag_role
from core.constant.maya.dag import attr as dag_attr

from core.constant.orbital import ghost as orbital_ghost


class LocatorNode(Node):
    """
    LocatorNode creates a locator in maya.
    This class acts as a string and can be printed, selected, and so on.
    This class subclasses DAG Node.
    """

    def __init__(self, guide_name, side, types: List, position: List[float], orientation: List[float]):
        # pre-compute locator name
        locator_types = types + [dag_role.LOCATOR]
        super().__init__(guide_name, side, locator_types, position, orientation)
        self.worldPosition_0 = f"{self}{dag_attr.WORLDPOSITION_0}"

    def create(self):
        loc_node = cmds.spaceLocator(name=self)
        cmds.xform(loc_node, t=self.position, ro=self.orientation)


class LocatorSet(List[LocatorNode]):
    """
    A collection of LimbLocatorSet indexed by their locator index and type.
    """

    def __init__(self, guide_names: List, side: str, types: List, positions: List[float], orientations: List[float]):
        super().__init__()
        group_types = types + [dag_role.GROUP]
        self.group = Node(guide_names[0], side, group_types, positions[0], orientations[0])

        # Pre-compute locators
        for i, (guide_name, position, orientation) in enumerate(zip(guide_names, positions, orientations)):
            i = f"{i+1:02d}"
            resolved_types = [(i if type is orbital_ghost.INDEX else type) for type in types]
            locator_node = LocatorNode(guide_name, side, resolved_types, position, orientation)
            self.append(locator_node)

    def create(self):
        # Create group node
        self.group.create()

        # Create guide positioned locators
        for loc in self:
            loc.create()
