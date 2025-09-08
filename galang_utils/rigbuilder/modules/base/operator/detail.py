from maya import cmds
from typing import List

from rigbuilder.constants.general import role as gen_role
from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup

from rigbuilder.cores.guide import ModuleInfo
from rigbuilder.modules.base.component.detail import DetailComponent
from rigbuilder.modules.base.operator.dg import Node


class DetailOperator(DetailComponent):
    def __init__(self, module: ModuleInfo, drivers: List, sub_divs: int, i: int):
        super().__init__(module, sub_divs, i)
        self.drivers = drivers

    def run(self):
        i = self.i
        sub_divs = self.sub_divs
        # STEP 0 : CONNECT DRIVERS TO ROOT JOINT AND IK HANDLE
        # Connect translation and rotation with constraint
        cmds.pointConstraint(self.drivers[i], self.root_joint, mo=True)
        cmds.pointConstraint(self.drivers[i + 1], self.ik_handle, mo=True)
        cmds.orientConstraint(self.drivers[i + 1], self.ik_handle, mo=True)

        # STEP 1 : CONNECT DRIVERS TO DETAIL CONTROLS CONSTRAINT LEVEL
        # Connect translation with constraint
        drivers = [self.drivers[i], self.drivers[i + 1]]
        for n in range(sub_divs):
            point_constraint = cmds.pointConstraint(drivers, self.controls[n].constraint)
            cmds.setAttr(f"{point_constraint}.{self.drivers[i]}WO", sub_divs - 1 - n)
            cmds.setAttr(f"{point_constraint}.{self.drivers[i +1]}W1", n)

            # STEP 2 : CONNECT END JOINT TO DETAIL JOINTS
            # Connect rotation with direct connect
            if n is not 0:
                multDiv = Node(self.guides[i], self.module, [role.DETAIL, gen_role.MULT_DL, n + 1])
                multDiv.create({"input2": n / sub_divs - 1})
                cmds.connectAttr(f"{self.end_joint}.rotate{self.axis}", f"{multDiv}.input1")
                cmds.connectAttr(f"{multDiv}.output", f"{self.joints[n]}.rotate{self.axis}")
