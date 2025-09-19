from typing import List
from maya import cmds
from core.component.dag import Node
from core.component.locator import LocatorNode, LocatorSet
from rig_x_frame.constants import constant_project as role


class BaseLocatorNode(LocatorNode):
    def __init__(self, base_name, side, labels: List, position: List[float], orientation: List[float]):
        labels.append(role.LOCATOR)
        super().__init__(base_name, side, labels, position, orientation)

    def create(self):
        self.create_locator()


class BaseLocatorSet(LocatorSet):
    def __init__(self, base_names: List, side: str, labels: List, positions: List[float], orientations: List[float]):
        labels.append(role.LOCATOR)
        super().__init__(base_names, side, labels, positions, orientations)
        self.group = Node(base_names[0], side, labels, positions[0], orientations[0])

    def create(self):
        self.create_locators()
        self.create_group()

    def create_group(self):
        self.group.create_node()
        for locator in self:
            cmds.parent(locator, self.group)
