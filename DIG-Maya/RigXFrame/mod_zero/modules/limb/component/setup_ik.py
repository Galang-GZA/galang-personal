from maya import cmds
from typing import Dict, List

from rig_x_frame.constants.general import role as gen_role
from rig_x_frame.constants.project import role as role
from rig_x_frame.mod_zero.limb.constant.format import LimbFormat

from rig_x_frame.core.guide import ModuleInfo
from rig_x_frame.mod_zero.base.component.dag import Node
from rig_x_frame.mod_zero.base.component.control import ControlSet
from core.component.joint import JointSet
from core.component.ik_handle import IkHandleNode
from rig_x_frame.mod_zero.base.component.locator import LocatorNode, LocatorSet


class LimbIKComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guides = module.guides
        self.control_guides = [self.guides[0], module.guides_pv, self.guides[-1]]

        self.group = Node(self.guides[0], module, [role.IK, role.RIG, role.GROUP])
        self.joints = JointSet(self.guides, module, [role.IK])
        self.controls = ControlSet(self.control_guides, module, [role.IK])
        self.locator = LocatorNode(self.guides[0], module, [role.IK])
        self.handle = IkHandleNode(
            guide=self.guides[0],
            module=module,
            source_joint=self.joints[0],
            end_effector=self.joints[-1],
            solver=gen_role.IK_RP_SOLVER,
            types=[role.DETAIL],
            position=self.guides[2].position,
        )

    def create(self):
        self.__create_core_ik_components()
        self.__parent_core_ik_components()
        self.__create_extra_ik_components()
        self.__parent_extra_ik_components()

    def __create_core_ik_components(self):
        components: List[Node] = [
            self.group,
            self.joints,
            self.controls,
            self.locator,
            self.handle,
        ]
        for component in components:
            component.create()

    def __create_extra_ik_components(self):
        self.static_locators = LocatorSet(self.guides, self.module, [role.IK, role.STATIC])
        self.active_locators = LocatorSet(self.control_guides, self.module, [role.IK, role.ACTIVE])
        self.base_locator = LocatorNode(self.control_guides[2], self.module, [role.IK, role.ACTIVE, role.BASE])
        self.blend_locator = LocatorNode(self.control_guides[2], self.module, [role.IK, role.ACTIVE, role.BLEND])
        self.stretch_locator = LocatorNode(self.control_guides[2], self.module, [role.IK, role.ACTIVE, role.STRETCH])
        components: List[Node] = [
            self.static_locators,
            self.active_locators,
            self.stretch_locator,
            self.base_locator,
            self.blend_locator,
        ]
        for component in components:
            component.create()

    def __parent_core_ik_components(self):
        children = [self.joints.group, self.controls.group, self.handle, self.locator]
        parents = [self.group, self.group, self.locator, self.controls[2]]
        for child, parent in zip(children, parents):
            cmds.parent(child, parent)

    def __parent_extra_ik_components(self):
        children = [self.active_locators[2], self.base_locator]
        parents = [self.active_locators[0], self.active_locators[0]]
        for child, parent in zip(children, parents):
            cmds.parent(child, parent)
