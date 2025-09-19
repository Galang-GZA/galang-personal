from maya import cmds
from typing import List
from core.component.dag import Node
from core.constant.maya.dag import role as dag_role
from core.constant.maya.dag import attr as dag_attr

from program.component import precompute_multiple_dag as precompute_locators


class LocatorNode(Node):
    """
    LocatorNode creates a locator in maya.
    This class acts as a string and can be printed, selected, and so on.
    This class subclasses DAG Node.
    """

    def __init__(self, base_name, side, labels: List, position: List[float], orientation: List[float]):
        # pre-compute locator name
        locator_types = labels + [dag_role.LOCATOR]
        super().__init__(base_name, side, locator_types, position, orientation)
        self.worldPosition_0 = f"{self}{dag_attr.WORLDPOSITION_0}"

    def create_locator(self):
        loc_node = cmds.spaceLocator(name=self)
        cmds.xform(loc_node, t=self.position, ro=self.orientation)


class LocatorSet(List[LocatorNode]):
    """
    A collection of LimbLocatorSet indexed by their locator index and type.
    """

    def __init__(
        self, base_names: List, side: str, labels: List, positions: List[List[float]], orientations: List[List[float]]
    ):
        super().__init__()
        self = precompute_locators.run(LocatorNode, base_names, side, labels, positions, orientations)

    def create_locators(self):
        # Create guide positioned locators
        for loc in self:
            loc.create()
