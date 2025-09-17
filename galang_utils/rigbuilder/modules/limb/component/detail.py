from maya import cmds
from typing import Dict, List

from rigbuilder.programs.sub_position import SubPositions
from rigbuilder.constants.general import role as gen_role
from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup

from rigbuilder.cores.guide import ModuleInfo
from rigbuilder.modules.base.component.dag import Node
from rigbuilder.modules.base.component.group import GroupNode
from core.component.joint import JointNode
from core.component.joint import JointSet
from rigbuilder.modules.base.component.control import ControlSet
from rigbuilder.modules.base.component.locator import LocatorNode
from core.component.ik_handle import IkHandleNode


"""PERTIMBANGIN BUTA TARUH DI MASING MASIH MODUL YANG BUTUH, GABUNGIN DI AKHIR SAAT PERLU OPTIMASI"""


class DetailComponent:
    def __init__(self, module: ModuleInfo, sub_divs: int, i: int):
        self.i = i
        self.module = module
        self.axis = module.axis
        self.sub_divs = sub_divs
        self.guides = module.guides
        self.div_guides = [self.guides[i]] * sub_divs
        self.positions = SubPositions(module, sub_divs, i).get()

        # Pre-compute upper details components
        self.group = GroupNode(self.guides[i], module, [role.DETAIL, role.GROUP])
        self.result_joints = JointSet(self.div_guides, module, [role.DETAIL, setup.INDEX], self.positions)
        self.root_joint = JointNode(self.guides[i], module, [role.DETAIL, role.IK, 1], self.positions[0])
        self.end_joint = JointNode(self.guides[i], module, [role.DETAIL, role.IK, 2], self.positions[-1])
        self.controls = ControlSet(self.div_guides, module, [role.DETAIL, setup.INDEX], self.positions)
        self.ik_locator = LocatorNode(self.guides[i], module, [role.DETAIL, role.IK], self.guides[i + 1].position)
        self.ik_effector = Node(self.guides[i], module, [role.DETAIL, role.EFFECTOR], self.guides[i + 1].position)
        self.ik_handle = IkHandleNode(
            guide=self.guides[i],
            module=module,
            source_joint=self.root_joint,
            end_effector=self.end_joint,
            solver=gen_role.IK_SC_SOLVER,
            types=[role.DETAIL],
            position=self.guides[i + 1].position,
        )

    def create(self):
        # Create pre-computed upper components
        components: List[Node] = [self.group, self.result_joints, self.controls, self.ik_locator, self.ik_handle]
        for component in components:
            component.create()

        # Parent upper components
        children = [self.ik_handle, self.ik_locator, self.result_joints.group, self.controls.group]
        parents = [self.ik_locator, self.group, self.group, self.group]
        for child, parent in zip(children, parents):
            cmds.parent(child, parent)

        # Parent detail result_joints to controls
        for joint, control in zip(self.result_joints, self.controls):
            cmds.parent(joint, control)
