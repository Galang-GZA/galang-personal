"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from typing import List
from core.component.dag import Node
from core.constant.maya.dag import role as dag_role
from core.constant.maya.dag import attr as dag_attr
from core.constant.orbital import ghost as orbital_ghost


class JointNode(Node):
    """
    LimbJointNode behaves like a string (the Maya node name) but also carries extra
    metadata (position, orientation, etc.) and has helper methods like create().
    """

    def __init__(self, guide_name, side, types: List, position: List[float], orientation: List[float]):
        # Pre-compute joint name
        joint_types = types + [role.JOINT]
        super().__init__(guide_name, side, joint_types, position, orientation)

    def create(self):
        """Creates the Maya joint"""
        cmds.select(clear=True)
        cmds.joint(name=self, position=self.position, orientation=self.orientation)


class JointSet(List[JointNode]):
    """
    LimbJointChain behaves like a list (consisting joints name) but also carries extra
    metadata (module, guides, etc.) and has helper methods like create().
    """

    def __init__(
        self,
        guide_names: List,
        side: str,
        types: List,
        positions: List[float],
        orientations: List[float],
        group_enabled: bool = True,
    ):
        super().__init__()
        # Pre compute group
        if group_enabled:
            group_types = types + [role.JOINT, role.GROUP]
            self.group = Node(guide_names[0], side, group_types, positions[0], orientations[0])

        # Pre-compute joints
        for i, (guide_name, position, orientation) in enumerate(zip(guide_names, positions, orientations)):
            i = f"{i+1:02d}"
            resolved_types = [(i if type is setup.INDEX else type) for type in types]
            jnt_node = JointNode(guide_name, side, resolved_types, position, orientation)
            self.append(jnt_node)

    def create(self):
        """Creates the Maya joints"""
        # Define and create top node
        if self.group:
            top_node = self.group.create()

        # Create each joint & parent accordingly
        for jnt_node in self:
            jnt_node.create()
            if top_node:
                cmds.parent(jnt_node, top_node)

            # Joint chaining
            top_node = jnt_node
