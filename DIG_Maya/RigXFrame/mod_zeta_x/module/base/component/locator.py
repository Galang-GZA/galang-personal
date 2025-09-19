from typing import List
from maya import cmds
from core.component.dag import Node
from core.component.locator import LocatorNode, LocatorSet
from RigXFrame.mod_zeta_x.constant import role


class BaseLocatorNode(LocatorNode):
    def __init__(self, base_name, side, labels: List, position: List[float], orientation: List[float]):
        labels.append(role.LOCATOR)
        super().__init__(base_name, side, labels, position, orientation)


class BaseLocatorSet(LocatorSet):
    def __init__(self, base_names: List, side: str, labels: List, positions: List[float], orientations: List[float]):
        labels.append(role.LOCATOR)
        super().__init__(base_names, side, labels, positions, orientations)

        # Precompute group
        group_labels = labels + [role.GROUP]
        self.group = Node(base_names[0], side, group_labels, positions[0], orientations[0])

    def create(self):
        # Create components then parent locators in the group
        self.group.create()
        for locator in self:
            locator.create()
            cmds.parent(locator, self.group)
