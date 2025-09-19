"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from typing import List
from core.component.dag import Node
from core.constant.maya.dag import role as dag_role
from core.constant.orbital import ghost as orbital_ghost

from program.component import precompute_multiple_dag as precompute_joints


class JointNode(Node):
    """
    LimbJointNode behaves like a string (the Maya node name) but also carries extra
    metadata (position, orientation, etc.) and has helper methods like create().
    """

    def __init__(self, base_name, side, labels: List, position: List[float], orientation: List[float]):
        super().__init__(base_name, side, labels, position, orientation)

    def create_joint(self):
        """Creates the Maya joint"""
        cmds.select(clear=True)
        cmds.joint(name=self, position=self.position, orientation=self.orientation)


class JointSet(List[JointNode]):
    """
    LimbJointChain behaves like a list (consisting joints name) but also carries extra
    metadata (module, guides, etc.) and has helper methods like create().
    """

    def __init__(
        self, base_names: List, side: str, labels: List, positions: List[List[float]], orientations: List[List[float]]
    ):
        super().__init__()
        self = precompute_joints.run(JointNode, base_names, side, labels, positions, orientations)

    def create_joints(self):
        """Creates the Maya joints"""
        # Create each joint & parent accordingly
        top_node = None
        for jnt_node in self:
            jnt_node.create()
            if top_node:
                cmds.parent(jnt_node, top_node)

            # Joint chaining
            top_node = jnt_node
