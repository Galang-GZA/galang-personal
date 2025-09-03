from maya import cmds
from typing import Dict, List

from rigbuilder.constants.general import role as gen_role
from rigbuilder.constants.project import role as role
from rigbuilder.modules.limb.constant.format import LimbFormat

from rigbuilder.cores.guide import ModuleInfo
from rigbuilder.modules.base.component.dag import Node
from rigbuilder.modules.base.component.group import GroupNode
from rigbuilder.modules.base.component.control import ControlSet
from rigbuilder.modules.base.component.joint_chain import JointChain
from rigbuilder.modules.base.component.ik_handle import IkHandleNode
from rigbuilder.modules.base.component.locator import LocatorNode, LimbLocatorSet


class LimbIKComponent:
    def __init__(self, module: ModuleInfo):
        self.guides = module.guides
        self.control_guides = [self.guides[0], module.guides_pv, self.guides[-1]]

        self.group = GroupNode(self.guides[0], module, [role.IK, role.RIG, role.GROUP])
        self.joints = JointChain(self.guides, module, [role.IK])
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

        self.static_locators = LimbLocatorSet(self.guides, module, [role.IK, role.STATIC])
        self.active_locators = LimbLocatorSet(self.control_guides, module, [role.IK, role.ACTIVE])
        self.base_locator = LocatorNode(self.control_guides[2], module, [role.IK, role.ACTIVE, role.BASE])
        self.blend_locator = LocatorNode(self.control_guides[2], module, [role.IK, role.ACTIVE, role.BLEND])
        self.stretch_locator = LocatorNode(self.control_guides[2], module, [role.IK, role.ACTIVE, role.STRETCH])

    def create(self):
        # Step 0: Create IK components
        components: List[Node] = [
            self.group,
            self.joints,
            self.controls,
            self.locator,
            self.handle,
            self.static_locators,
            self.active_locators,
            self.stretch_locator,
            self.base_locator,
            self.blend_locator,
        ]
        for component in components:
            component.create()

        # Step 1 : Parent IK Components
        children = [self.active_locators[2], self.base_locator, self.handle, self.locator]
        parents = [self.active_locators[0], self.active_locators[0], self.locator, self.controls[2]]
        for child, parent in zip(children, parents):
            cmds.parent(child, parent)

        # Step 2: Setup IK attributes
        # Add attributes for soft, stretch, pin, slide
        cmds.setAttr("ikRPsolver.tolerance", 1e-007)
        attrs = {
            role.SOFT: [0.0001, 100, 0.0001],
            role.STRETCH: [0.0, 1.0, 0.0],
            role.PIN: [0.0, 1.0, 0.0],
            role.SLIDE: [-1.0, 1.0, 0.0],
        }
        for attr, (min_val, max_val, default_val) in attrs.items():
            if not cmds.attributeQuery(attr, node=self.controls[2], exists=True):
                cmds.addAttr(self.controls[2], ln=attr, at="double", dv=default_val, k=True, min=min_val, max=max_val)
