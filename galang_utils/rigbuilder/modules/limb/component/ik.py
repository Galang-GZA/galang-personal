from maya import cmds
from typing import Dict, List

from galang_utils.rigbuilder.constant.general import role as general_role
from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat

from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.base.component.group import GroupNode
from galang_utils.rigbuilder.modules.base.component.control import ControlSet
from rigbuilder.modules.base.component.joint_chain import JointChain
from rigbuilder.modules.base.operator.distance import DistanceSet
from galang_utils.rigbuilder.modules.base.component.locator import LocatorNode, LimbLocatorSet


class LimbIKComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.guide = module.guide
        self.guides = module.guides
        self.format = LimbFormat(self.guide.side, role.IK)

        self.group = GroupNode(self.guide, module, [role.IK, role.RIG, role.GROUP])
        self.joints = JointChain(self.guides, module, [role.IK])
        self.controls = ControlSet(self.guides, module, [role.IK])
        self.loc_handle = LocatorNode(module.guide, module, [role.IK])
        self.handle = None

        self.static_locators = LimbLocatorSet(module, [role.IK, role.STATIC])
        self.static_distances = DistanceSet(module, [role.IK, role.STATIC])
        self.active_locators = LimbLocatorSet(module, [role.IK, role.ACTIVE])
        self.active_distances = DistanceSet(module, [role.IK, role.ACTIVE])

    def create(self):
        print(f"update {self.module.guide.name} success")
        # Step 0: Create IK components
        self.group.create()
        self.joints.create()
        self.controls.create()
        self.static_locators.create()
        self.static_distances.create()
        self.active_locators.create()
        self.active_distances.create()

        # Step 1: Setup IK attributes
        # Add attributes for soft, stretch, pin, slide
        ik_ctrl = self.controls[2]
        pv_ctrl = self.controls[1]
        attrs = {
            role.SOFT: [0.0001, 100, 0.0001],
            role.STRETCH: [0.0, 1.0, 0.0],
            role.PIN: [0.0, 1.0, 0.0],
            role.SLIDE: [-1.0, 1.0, 0.0],
        }
        for attr, (min_val, max_val, default_val) in attrs.items():
            if not cmds.attributeQuery(attr, node=ik_ctrl, exists=True):
                cmds.addAttr(ik_ctrl, ln=attr, at="double", dv=default_val, keyable=True, min=min_val, max=max_val)

        # Step 2: Re - parent active locators
        cmds.parent(self.active_locators[2], self.active_locators[0])
        cmds.parent(self.active_locators.base, self.active_locators[0])

        # Step 3: Create IK handle
        ik_handle_name = self.format.name(self.guide.name_raw)
        ik_solver_name = self.format.name(self.guide.name_raw, item="RPsolver")
        self.handle = cmds.ikHandle(n=ik_handle_name, sj=self.joints[0], ee=self.joints[2], sol="ikRPsolver")[0]

        cmds.rename("effector1", ik_solver_name)
        cmds.setAttr("ikRPsolver.tolerance", 1e-007)
        cmds.parent(self.handle, self.loc_handle)
        cmds.parent(self.loc_handle, ik_ctrl)
        cmds.poleVectorConstraint(pv_ctrl, self.handle)
