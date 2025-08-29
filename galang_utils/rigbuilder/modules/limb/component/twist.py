from maya import cmds
from typing import Dict, List

from galang_utils.rigbuilder.constant.general import role as gen_role
from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.constant.project import setup as setup

from galang_utils.rigbuilder.core.guide import ModuleInfo, GuideInfo
from rigbuilder.modules.base.component.dag import Node
from galang_utils.rigbuilder.modules.base.component.group import GroupNode
from rigbuilder.modules.base.component.joint_chain import JointChain
from galang_utils.rigbuilder.modules.base.component.control import ControlSet
from galang_utils.rigbuilder.modules.base.component.locator import LocatorNode
from galang_utils.rigbuilder.modules.base.component.ik_handle import IkHandleNode


class LimbBendyComponent:
    def __init__(self, module: ModuleInfo, sub_divs: int):
        self.module = module
        self.guide = module.guide
        self.guides = module.guides

        # Pre-compute group sub rig group node
        self.group = GroupNode(self.guide, module, [role.ROLL, role.RIG, role.GROUP])

        # ------------------- Partial Method -------------------
        # Pre-compute upper details components
        upper_positions = self._get_sub_positions(self.guides[0], sub_divs)
        self.up_guides = [self.guides[0]] * sub_divs
        self.up_group = GroupNode(self.guides[0], module, [role.ROLL, role.GROUP])
        self.up_joints = JointChain(self.up_guides, module, [role.ROLL], True, upper_positions)
        self.up_controls = ControlSet(self.up_guides, module, [role.ROLL], True, upper_positions)
        self.up_ik_locator = LocatorNode(self.guides[0], module, [role.ROLL, role.IK], self.guides[1].position)
        self.up_ik_effectr = Node(self.guides[0], module, [role.ROLL, role.EFFECTOR], self.guides[1].position)
        self.up_ik_handle = IkHandleNode(
            guide=self.guides[0],
            module=module,
            source_joint=self.up_joints[0],
            end_effector=self.up_joints[1],
            solver=gen_role.IK_SC_SOLVER,
            effector=self.up_ik_effectr,
            types=[role.ROLL],
        )

        # Pre-compute lower details components
        lower_positions = self._get_sub_positions(self.guides[1], sub_divs)
        self.low_guides = [self.guides[1]] * sub_divs
        self.low_group = GroupNode(self.guides[1], module, [role.ROLL, role.GROUP])
        self.low_joints = JointChain(self.low_guides, module, role.ROLL, True, lower_positions)
        self.low_controls = ControlSet(self.low_guides, module, role.ROLL, True, lower_positions)
        self.low_ik_locator = LocatorNode(self.guides[1], module, [role.ROLL, role.IK], self.guides[2].position)
        self.low_ik_effectr = Node(self.guides[1], module, [role.ROLL, role.EFFECTOR], self.guides[2].position)
        self.low_ik_handle = IkHandleNode(
            guide=self.guides[1],
            module=module,
            source_joint=self.low_joints[0],
            end_effector=self.low_joints[1],
            solver=gen_role.IK_SC_SOLVER,
            effector=self.up_ik_effectr,
            types=[role.ROLL],
        )

        # ------------------- Loop Method -------------------
        # Pre-compute roll and detail components
        partial_guides = [[guide] * sub_divs for guide in self.guides.pop()]
        positions = [self._get_sub_positions(guide, sub_divs) for guide in self.guides.pop()]
        pairs = list(zip(partial_guides, positions))
        self.partial_groups = [GroupNode(g, module, [role.ROLL, role.GROUP]) for g in partial_guides]
        self.controls = [ControlSet(g, module, role.ROLL, True, p) for g, p in pairs]
        self.joints = [JointChain(g, module, role.ROLL, True, p) for g, p in pairs]
        self.ik_locators = [LocatorNode(g, module, [role.ROLL, role.IK], p[-1]) for g, p in pairs]
        self.ik_effectors = [Node(g, module, [role.ROLL, role.EFFECTOR], p[-1]) for g, p in pairs]
        self.ik_handles = [Node(g, module, [role.ROLL, role.IK], p[-1]) for g, p in pairs]
        self.up_ik_handle = [
            IkHandleNode(
                guide=guide,
                module=module,
                source_joint=self.joints[i].sub_root,
                end_effector=self.joints[i].sub_end,
                solver=gen_role.IK_SC_SOLVER,
                effector=self.ik_effectors[i],
                types=[role.ROLL],
                position=position[-1],
            )
            for i, (guide, position), position in enumerate(pairs)
        ]

    def _get_sub_positions(self, guide: GuideInfo, sub_divs):
        index = self.guides.index(guide)
        root_position = guide.position
        end_position = self.guides[index + 1].position
        sub_positions: List = None
        for i in range(sub_divs):
            ratio = i / sub_divs
            sub_position = [root_position[n] + ratio * (end_position[n] - root_position[n]) for n in range(3)]
            sub_positions.append(sub_position)

        return sub_positions

    def create(self):
        # Create main group
        self.group.create()

        # ------------------- Partial Method -------------------
        # -------------------
        # Create pre-computed upper components
        self.up_group.create()
        self.up_joints.create()
        self.up_controls.create()
        self.up_ik_locator.create()
        self.up_ik_handle.create()

        # Parent upper components
        cmds.parent(self.up_ik_handle, self.up_ik_locator)
        cmds.parent(self.up_ik_locator, self.up_group)
        cmds.parent(self.up_joints.group, self.up_group)
        cmds.parent(self.up_controls.group, self.up_group)
        cmds.parent(self.up_group, self.group)

        # Parent upper roll joints to detail controls
        for joint, control in zip(self.up_joints, self.up_controls):
            cmds.parent(joint, control)

        # -------------------
        # Create pre-computed lower components
        self.low_group.create()
        self.low_joints.create()
        self.low_controls.create()
        self.low_ik_locator.create()
        self.up_ik_handle.create()

        # Parent llowerow components
        cmds.parent(self.low_ik_handle, self.low_ik_locator)
        cmds.parent(self.low_ik_locator, self.low_group)
        cmds.parent(self.low_joints.group, self.low_group)
        cmds.parent(self.low_controls.group, self.low_group)
        cmds.parent(self.low_group, self.group)

        # Parent lower roll joints to detail controls
        for joint, control in zip(self.low_joints, self.low_controls):
            cmds.parent(joint, control)

        # ------------------- One Loop Method -------------------
        # Create components
        for i in range(len(self.guides.pop())):
            self.partial_groups[i].create()
            self.joints[i].create()
            self.ik_locators[i].create()
            self.controls[i].create()
            self.ik_handles[i].create()

            # Parent components to partial groups
            cmds.parent(self.ik_handles[i], self.ik_locators[i])
            cmds.parent(self.joints[i].group, self.partial_groups[i])
            cmds.parent(self.ik_locators[i], self.partial_groups[i])
            cmds.parent(self.controls[i].group, self.partial_groups[i])
            cmds.parent(self.partial_groups[i], self.group)

            # Parent roll joints to detail controls
            for joint, control in zip(self.joints[i], self.controls[i]):
                cmds.parent(joint, control)
