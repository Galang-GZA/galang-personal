from typing import List
from maya import cmds
from core.component.dag import Node
from core.component.joint import JointNode, JointSet
from RigXFrame.mod_zeta_x.constant import role


class BaseJointNode(JointNode):
    def __init__(self, base_name, side, labels: List, position: List[float], orientation: List[float]):
        labels.append(role.JOINT)
        super().__init__(base_name, side, labels, position, orientation)


class BaseJointSet(JointSet):
    def __init__(self, base_names: List, side: str, labels: List, positions: List[float], orientations: List[float]):
        labels.append(role.JOINT)
        super().__init__(base_names, side, labels, positions, orientations)

        # Precompute group
        group_labels = labels + [role.GROUP]
        self.group = Node(base_names[0], side, group_labels, positions[0], orientations[0])

    def create(self, group_enabled: bool = True):
        # Create each joint, group & parent accordingly
        if group_enabled:
            self.group.create()
            top_node = self.group
        else:
            top_node = None

        for jnt_node in self:
            jnt_node.create()
            if top_node:
                cmds.parent(jnt_node, top_node)

            # Joint chaining
            top_node = jnt_node
