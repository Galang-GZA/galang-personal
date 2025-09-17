from maya import cmds
from typing import List
from rigbuilder.constants.project import role as role
from rigbuilder.constants.general import role as gen_role
from rigbuilder.cores.guide import GuideInfo, ModuleInfo
from rigbuilder.modules.base.component.dag import Node


class IkHandleNode(Node):
    """
    LimbIkHandleeNode behaves like a string (the Maya node name) but also carries
    helper methods like create().
    """

    def __init__(
        self,
        guide_name: str,
        side: str,
        source_joint: str,
        end_effector: str,
        solver: str,
        types: List,
        position: List[float],
        orientation: List[float],
    ):
        self.solver = solver
        self.source_joint = source_joint
        self.end_effector = end_effector
        ik_handle_types = types + [role.IK]
        effector_types = types + [role.EFFECTOR]
        self.effector = Node(guide_name, side, effector_types, position, orientation)
        super().__init__(guide_name, side, ik_handle_types, position, orientation)

    def create(self):
        """
        Creates the ik handle.
        """
        ik_handle = cmds.ikHandle(n=self, sj=self.source_joint, ee=self.end_effector, sol=self.solver)[0]
        cmds.rename(gen_role.EFFECTOR1, self.effector)
        return ik_handle
