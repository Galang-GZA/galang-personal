from maya import cmds
from typing import Dict, List

from galang_utils.rigbuilder.constant.general import role as gen_role
from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat

from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.base.component.dag import Node
from galang_utils.rigbuilder.modules.base.component.group import GroupNode
from galang_utils.rigbuilder.modules.base.component.control import ControlSet
from galang_utils.rigbuilder.modules.base.component.joint_chain import JointChain
from galang_utils.rigbuilder.modules.base.component.ik_handle import IkHandleNode
from rigbuilder.modules.base.operator.distance import DistanceNode, DistanceSet
from galang_utils.rigbuilder.modules.base.component.locator import LocatorNode, LimbLocatorSet


class IKComponent:
    def __init__(self, module: ModuleInfo):
        guides = module.guides

        self.static_distances = DistanceSet(guides, module, [role.IK, role.STATIC])
        self.active_distances = DistanceSet(guides, module, [role.IK, role.ACTIVE])
        self.stretch_locator = DistanceNode(guides[2], module, [role.IK, role.ACTIVE, role.STRETCH])
        self.base_locator = DistanceNode(guides[2], module, [role.IK, role.ACTIVE, role.BASE])
        self.blend_locator = DistanceNode(guides[2], module, [role.IK, role.ACTIVE, role.BLEND])

    def create(self):
        pass
        cmds.poleVectorConstraint(pv_ctrl, self.ik_handle)
