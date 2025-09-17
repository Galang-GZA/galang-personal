from maya import cmds
from typing import Dict, Union

from rigbuilder.constants.general import role as gen_role
from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup

from rigbuilder.modules.limb.operator.detail import DetailOperator
from rigbuilder.modules.limb.component.setup_detail import LimbDetailComponent
from rigbuilder.modules.limb.component.zcomponents import LimbComponents


class LimbDetailOperator:
    def __init__(self, components: LimbComponents):
        self.components = components

    def run(self):
        drivers = self.components.result.joints
        upper_detail = self.components.detail.upper
        lower_detail = self.components.detail.lower
        DetailOperator(upper_detail, drivers).run()
        DetailOperator(lower_detail, drivers).run()


# class LimbDetailOperator:
#     def __init__(self, component: LimbComponent):
#         self.guides = component.module.guides
#         self.detail = component.detail
#         self.axis = component.module.axis
#         self.side = component.module.side
#         self.driver = None
#         self.format = LimbFormat(component.module.side)

#     def run(self):
#         # Connect manipulator to ik handle
#         if cmds.ls(f"*{role.RESULT}*"):
#             self.driver = self.component.result

#         LEN_INDEX = setup.SUB_DIVS - 1
#         for i in range(len(self.guides) - 1):
#             ik_root_jnt = self.sub.joints[self.guides[i]][role.IK][0]
#             ik_handle = self.sub.handles[self.guides[i]]
#             ik_root_driver = self.driver.joints[i]
#             ik_handle_driver = self.driver.joints[i + 1]

#             cmds.pointConstraint(ik_root_driver, ik_root_jnt)
#             cmds.parentConstraint(ik_handle_driver, ik_handle)

#             # Connect ik roll joint's rotation to roll joint's rotation to detail controls to roll controls
#             roll_root = self.sub.joints[self.guides[i]][0]
#             roll_end = self.sub.joints[self.guides[i]][LEN_INDEX]

#             for n in range(setup.SUB_DIVS):
#                 roll_jnt = self.sub.joints[self.guides[i]][n]
#                 roll_manipulator = self.sub.controls[self.guides[i]][role.ROLL][n]
#                 detail_manipulator = self.sub.controls[self.guides[i]][role.DETAIL][n]
#                 ratio = n / LEN_INDEX if LEN_INDEX != 0 else 0

#                 # Connect end roll joint to ik handle driver
#                 if n == LEN_INDEX:
#                     cmds.pointConstraint(ik_handle_driver, roll_jnt)

#                 # Connect translate
#                 if 0 < n < LEN_INDEX:
#                     pos_node_name = self.format.name(
#                         self.guides[i].name_raw, role.MULT_DIV, role.ROLL, role.POSITION, index=n
#                     )
#                     pos_node = cmds.createNode("multDoubleLinear", n=pos_node_name)
#                     cmds.setAttr(f"{pos_node}.input1", ratio)
#                     cmds.connectAttr(f"{roll_end}.translate{self.axis}", f"{pos_node}.input2")
#                     cmds.connectAttr(f"{pos_node}.output", f"{roll_jnt}.translate{self.axis}")

#                 # Connect Rotation
#                 if n < LEN_INDEX:
#                     orient_node_name = self.format.name(
#                         self.guides[i].name_raw, role.MULT_DIV, role.ROLL, role.ORIENT, index=n
#                     )
#                     orient_node = cmds.createNode("multDoubleLinear", n=orient_node_name)
#                     cmds.setAttr(f"{orient_node}.input1", ratio - 1)
#                     cmds.connectAttr(f"{ik_root_jnt}.rotate{self.axis}", f"{orient_node}.input2")
#                     cmds.connectAttr(f"{orient_node}.output", f"{roll_jnt}.rotate{self.axis}")

#                 # Connect joint to control
#                 cmds.parentConstraint(roll_jnt, roll_manipulator.top)

#                 # Connect control detail to roll
#                 cmds.parentConstraint(roll_manipulator.ctrl, detail_manipulator.top)
