from maya import cmds
from typing import List

from rig_x_frame.constants.general import role as gen_role
from rig_x_frame.constants.project import role as role
from rig_x_frame.constants.project import setup as setup

from rig_x_frame.mod_zero.limb.component.detail import DetailComponent
from rig_x_frame.mod_zero.base.operator.dg import Node


class DetailOperator:
    def __init__(self, components: DetailComponent, drivers: List):
        self.components = components
        self.drivers = drivers

    def run(self):
        i = self.components.i
        axis = self.components.axis
        module = self.components.module
        guides = self.components.guides
        sub_divs = self.components.sub_divs

        result_joints = self.components.result_joints
        root_joint = self.components.root_joint
        end_joint = self.components.end_joint
        ik_handle = self.components.ik_handle
        controls = self.components.controls

        # STEP 0 : CONNECT DRIVERS TO ROOT JOINT AND IK HANDLE
        # Connect translation and rotation with constraint
        cmds.pointConstraint(self.drivers[i], root_joint, mo=True)
        cmds.pointConstraint(self.drivers[i + 1], ik_handle, mo=True)
        cmds.orientConstraint(self.drivers[i + 1], ik_handle, mo=True)

        # STEP 1 : CONNECT DRIVERS TO DETAIL CONTROLS CONSTRAINT LEVEL
        # Connect translation with constraint
        drivers = [self.drivers[i], self.drivers[i + 1]]
        for n in range(sub_divs):
            point_constraint = cmds.pointConstraint(drivers, controls[n].constraint)
            cmds.setAttr(f"{point_constraint}.{self.drivers[i]}WO", sub_divs - 1 - n)
            cmds.setAttr(f"{point_constraint}.{self.drivers[i +1]}W1", n)

            # STEP 2 : CONNECT END JOINT TO DETAIL JOINTS
            # Connect rotation with direct connect
            if n is not 0:
                multDiv = Node(guides[i], module, [role.DETAIL, gen_role.MULT_DL, n + 1])
                multDiv.create({"input2": n / sub_divs - 1})
                cmds.connectAttr(f"{end_joint}.rotate{axis}", f"{multDiv}.input1")
                cmds.connectAttr(f"{multDiv}.output", f"{result_joints[n]}.rotate{axis}")
