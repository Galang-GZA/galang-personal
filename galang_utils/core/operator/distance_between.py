from maya import cmds
from typing import List, Dict
from core.constant.orbital import ghost as orbital_ghost
from core.constant.maya.dg import role as dg_role
from core.constant.maya.dg import attr as dg_attr
from core.component.locator import LocatorNode
from core.operator.dg import Node, NodeSet


class DistanceBetween(Node):
    """
    Represents a Maya distanceBetween node.

    Subclass of Node that defines `node_type` and adds
    convenient properties for inputs/outputs.
    """

    node_type = dg_role.DISTANCE_BETWEEN

    def __init__(self, base_name: str, side: str, labels: List):
        super().__init__(base_name, side, labels)

        # Input Attributes
        self.point1 = f"{self}{dg_attr.INPUT1}"
        self.point2 = f"{self}{dg_attr.INPUT2}"

        # Outputs Attributes
        self.distance = f"{self}.{dg_attr.DISTANCE}"


class DistanceSet(NodeSet[DistanceBetween]):
    """
    Represents a list of multDoubleLinear nodes.

    Subclass of NodeSet bound to MultDoubleLinear.
    Automatically creates multiple nodes with indexed labels if required.
    """

    def __init__(self, base_names: List, side, labels: List):
        super().__init__(base_names, side, labels)


class ConnectDistances:
    """
    ConnectDistances connects multiple distanceBetween to pairs of locator nodes.
    Each DistanceNode must be associated with exactly 2 LocatorNodes.
    """

    def __init__(self, distances_and_locators: Dict[DistanceBetween, List[LocatorNode]]):
        self.distances: List[DistanceBetween] = list(distances_and_locators.keys())
        self.locators1: List[LocatorNode] = [locs[0] for locs in distances_and_locators.values()]
        self.locators2: List[LocatorNode] = [locs[1] for locs in distances_and_locators.values()]

    def run(self):
        for distance, locator1, locator2 in zip(self.distances, self.locators1, self.locators2):
            cmds.connectAttr(locator1.worldPosition_0, distance.point1, force=True)
            cmds.connectAttr(locator2.worldPosition_0, distance.point2, force=True)
