"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from typing import List
from rigbuilder.constant.project import role as role
from rigbuilder.constant.project import setup as setup
from rigbuilder.constant.general import role as gen_role
from rigbuilder.modules.base.component.group import GroupNode
from rigbuilder.core.guide import GuideInfo, ModuleInfo
from rigbuilder.modules.base.component.dag import Node


class JointNode(Node):
    """
    LimbJointNode behaves like a string (the Maya node name) but also carries extra
    metadata (position, orientation, etc.) and has helper methods like create().
    """

    def __init__(
        self,
        guide: GuideInfo,
        module: ModuleInfo,
        types: List = None,
        position: List[float] = None,
    ):
        # Pre-compute joint name
        joint_types = types.append(role.JOINT)
        super().__init__(guide, module, joint_types, position)

    def create(self):
        """
        Creates the Maya joint.
        """
        cmds.select(clear=True)
        jnt_node = cmds.joint(name=self, position=self.position, orientation=self.orientation)
        cmds.setAttr(f"{jnt_node}.{gen_role.SIDE}", self.module.side_id)
        return jnt_node


class JointChain(List[JointNode]):
    """
    LimbJointChain behaves like a list (consisting joints name) but also carries extra
    metadata (module, guides, etc.) and has helper methods like create().
    """

    def __init__(
        self,
        guides,
        module: ModuleInfo,
        types: List,
        positions: List = None,
        group_enabled: bool = True,
    ):
        super().__init__()
        # Pre compute group
        if group_enabled:
            group_types = types.append(role.JOINT, role.GROUP)
            self.group = GroupNode(guides[0], module, group_types)

        # Pre-compute joints
        for i, (guide, position) in enumerate(zip(guides, positions)):
            i = f"{i+1:02d}"
            resolved_types = [(i if t is setup.INDEX else t) for t in types]
            jnt_node = JointNode(guide, module, resolved_types, position)
            self.append(jnt_node)

    def create(self):
        """
        Creates the Maya joints.
        """
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
