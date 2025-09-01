from maya import cmds
from typing import Dict, List

from rigbuilder.constant.general import role as gen_role
from rigbuilder.constant.project import role as role
from rigbuilder.constant.project import setup as setup

from rigbuilder.core.guide import ModuleInfo, GuideInfo
from rigbuilder.modules.base.component.dag import Node
from rigbuilder.modules.base.component.group import GroupNode
from rigbuilder.modules.base.component.joint_chain import JointNode
from rigbuilder.modules.base.component.joint_chain import JointChain
from rigbuilder.modules.base.component.control import ControlSet
from rigbuilder.modules.base.component.locator import LocatorNode
from rigbuilder.modules.base.component.ik_handle import IkHandleNode


class DetailComponent:
    def __init__(self, module: ModuleInfo, sub_divs: int, i: int):
        guides = module.guides
        div_guides = [guides[i]] * sub_divs
        positions = self._get_sub_positions(module, sub_divs, i)

        # Pre-compute upper details components
        self.group = GroupNode(guides[i], module, [role.DETAIL, role.GROUP])
        self.joints = JointChain(div_guides, module, [role.DETAIL, setup.INDEX], positions)
        self.root_joint = JointNode(guides[i], module, [role.DETAIL, role.IK, 1], positions[0])
        self.end_joint = JointNode(guides[i], module, [role.DETAIL, role.IK, 2], positions[-1])
        self.controls = ControlSet(div_guides, module, [role.DETAIL, setup.INDEX], positions)
        self.ik_locator = LocatorNode(guides[i], module, [role.DETAIL, role.IK], guides[i + 1].position)
        self.ik_effector = Node(guides[i], module, [role.DETAIL, role.EFFECTOR], guides[i + 1].position)
        self.ik_handle = IkHandleNode(
            guide=guides[i],
            module=module,
            source_joint=self.root_joint,
            end_effector=self.end_joint,
            solver=gen_role.IK_SC_SOLVER,
            types=[role.DETAIL],
            position=guides[i + 1].position,
        )

    def _get_sub_positions(self, module: ModuleInfo, sub_divs: int, i: int):
        root_position = module.guides[i].position
        end_position = module.guides[i + 1].position
        detail_positions: List = None
        for i in range(sub_divs):
            ratio = i / sub_divs
            detail_position = [root_position[n] + ratio * (end_position[n] - root_position[n]) for n in range(3)]
            detail_positions.append(detail_position)

        return detail_positions

    def create(self):
        # Create pre-computed upper components
        components: List[Node] = [self.group, self.joints, self.controls, self.ik_locator, self.ik_handle]
        for component in components:
            component.create()

        # Parent upper components
        children = [self.ik_handle, self.ik_locator, self.joints.group, self.controls.group]
        parents = [self.ik_locator, self.group, self.group, self.group]
        for child, parent in zip(children, parents):
            cmds.parent(child, parent)

        # Parent detail joints to controls
        for joint, control in zip(self.joints, self.controls):
            cmds.parent(joint, control)
