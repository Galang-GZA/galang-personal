from typing import List
from maya import cmds
from core.component.dag import Node
from core.component.ik_handle import IkHandleNode
from rig_x_frame.constants import constant_project as role


class BaseIkHandleNode(IkHandleNode):
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
        labels.append(role.IK)
        super().__init__(base_name, side, source_joint, end_effector, solver, labels, position, orientation)

    def create(self):
        self.create_ik()
