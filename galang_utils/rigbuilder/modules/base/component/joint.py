from typing import List
from maya import cmds
from core.component.dag import Node
from core.component.joint import JointNode, JointSet
from rigbuilder.constants import constant_project as role


class BaseJointNode(JointNode):
    def __init__(self, base_name, side, labels: List, position: List[float], orientation: List[float]):
        labels.append(role.JOINT)
        super().__init__(base_name, side, labels, position, orientation)

    def create(self):
        self.create_joint()


class BaseJointSet(JointSet):
    def __init__(
        self,
        base_names: List,
        side: str,
        labels: List,
        positions: List[float],
        orientations: List[float],
        group_enabled: bool = False,
    ):
        labels.append(role.JOINT)
        super().__init__(base_names, side, labels, positions, orientations)
        self.group_enabled = group_enabled
        if group_enabled:
            self.group = Node(base_names[0], side, labels, positions[0], orientations[0])

    def create(self):
        self.create_joints()
        if self.group_enabled:
            self.create_group()

    def create_group(self):
        self.group.create_node()
        cmds.parent(self[0], self.group)
