from maya import cmds
from typing import List
from rigbuilder.constant.project import role as role
from rigbuilder.constant.general import role as gen_role
from rigbuilder.core.guide import GuideInfo, ModuleInfo
from rigbuilder.modules.base.component.dag import Node


class IkHandleNode(Node):
    """
    LimbIkHandleeNode behaves like a string (the Maya node name) but also carries
    helper methods like create().
    """

    def __init__(
        self,
        guide: GuideInfo,
        module: ModuleInfo,
        source_joint: str,
        end_effector: str,
        solver: str,
        types: List = None,
        position: List[float] = None,
    ):
        self.solver = solver
        self.source_joint = source_joint
        self.end_effector = end_effector
        ik_handle_types = types.append(role.IK)
        self.effector = Node(guide, module, [role.DETAIL, role.EFFECTOR], position)
        super().__init__(guide, module, ik_handle_types, position)

    def create(self):
        """
        Creates the ik handle.
        """
        ik_handle = cmds.ikHandle(n=self, sj=self.source_joint, ee=self.end_effector, sol=self.solver)[0]
        cmds.rename(gen_role.EFFECTOR1, self.effector)
        return ik_handle
