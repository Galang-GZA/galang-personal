from maya import cmds
from typing import List
from core.constant.orbital.format import DIG_Format
from core.constant.maya.dag import role as maya_role
from core.component.dag import Node


class IkHandleNode(Node):
    """
    LimbIkHandleeNode behaves like a string (the Maya node name) but also carries
    helper methods like create().
    """

    def __init__(
        self,
        base_name: str,
        side: str,
        source_joint: str,
        end_effector: str,
        solver: str,
        labels: List,
        position: List[float],
        orientation: List[float],
    ):
        super().__init__(base_name, side, labels, position, orientation)
        self.solver = solver
        self.source_joint = source_joint
        self.end_effector = end_effector
        self.effector = DIG_Format(side, base_name, labels).name()

    def create_ik(self):
        """
        Creates the ik handle.
        """
        ik_handle = cmds.ikHandle(n=self, sj=self.source_joint, ee=self.end_effector, sol=self.solver)[0]
        cmds.rename(maya_role.EFFECTOR1, self.effector)
        return ik_handle
