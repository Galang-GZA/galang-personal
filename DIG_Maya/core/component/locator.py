from maya import cmds
from typing import List
from core.component.dag import Node
from core.constant.maya.dag import role as dag_role
from core.constant.maya.dag import attr as dag_attr
from core.support.node import precompute_multiple_dag as precompute_locators


class LocatorNode(Node):
    """
    This class creates a dag locator node in Maya and behaves like a string.
    Subclass of `Node` that adds a shortcut to its attributes.
    """

    def __init__(self, base_name, side, labels: List, position: List[float], orientation: List[float]):
        super().__init__(base_name, side, labels, position, orientation)

        # Attribute
        self.worldPosition_0 = f"{self}{dag_attr.WORLDPOSITION_0}"

    def create(self):
        # Create locator in Maya
        locator_node = cmds.spaceLocator(name=self)[0]
        cmds.xform(locator_node, t=self.position, ro=self.orientation)
        return locator_node


class LocatorSet(List[LocatorNode]):
    """
    This class creates a list of locatorNodes with indexing support behaves like a list.
    """

    def __init__(
        self, base_names: List, side: str, labels: List, positions: List[List[float]], orientations: List[List[float]]
    ):
        super().__init__()
        locators = precompute_locators.run(LocatorNode, base_names, side, labels, positions, orientations)
        self.extend(locators)

    def create(self):
        # Create guide positioned locators
        for loc in self:
            loc.create()
