"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from typing import List
from core.component.dag import Node
from core.support.node import precompute_multiple_dag as precompute_joints


class JointNode(Node):
    """
    This class creates a dag joint node in Maya and behaves like a string.
    Subclass of `Node` that adds a shortcut to its attributes.
    """

    def __init__(self, base_name, side, labels: List, position: List[float], orientation: List[float]):
        super().__init__(base_name, side, labels, position, orientation)

    def create(self):
        # Create Joint in Maya
        cmds.select(clear=True)
        joint_node = cmds.joint(name=self, position=self.position, orientation=self.orientation)
        return joint_node


class JointSet(List[JointNode]):
    """
    This class creates a list of joints with indexing support and behaves like a list.
    """

    def __init__(
        self, base_names: List, side: str, labels: List, positions: List[List[float]], orientations: List[List[float]]
    ):
        super().__init__()
        joints = precompute_joints.run(JointNode, base_names, side, labels, positions, orientations)
        self.extend(joints)

    def create(self):
        # Create each joint & parent accordingly
        top_node = None
        for jnt_node in self:
            jnt_node.create()
            if top_node:
                cmds.parent(jnt_node, top_node)

            # Joint chaining
            top_node = jnt_node
