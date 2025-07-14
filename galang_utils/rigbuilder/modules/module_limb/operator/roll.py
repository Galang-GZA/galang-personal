from maya import cmds
from typing import Dict, Union
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_limb.rule.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.component.zcomponent import *


class LimbRollOperator:
    def __init__(self, component: LimbComponent):
        self.component = component
        self.module = component.roll.module

    def run(self):
        # Connect manipulator to ik handle
        guides = self.module.guides + self.module.guides_end
        axis = self.module.axis
        roll = self.component.roll
        side = self.module.guide.side
        driver = None

        if cmds.ls(f"*{RESULT}*"):
            driver = self.component.result

        LEN_INDEX = LEN_DETAILS - 1
        for index, g in enumerate(guides):
            if not index == LEN_INDEX:
                roll_ik_root = roll.joints[f"{g.name}{IK}0"]
                roll_ik_handle = roll.handles[g.name]
                roll_root_ik_driver = driver.map[g.name][JNT]
                roll_handle_ik_driver = driver.map[guides[index + 1].name][JNT]

                if roll_ik_handle:
                    cmds.pointConstraint(roll_root_ik_driver, roll_ik_root)
                    cmds.parentConstraint(roll_handle_ik_driver, roll_ik_handle)

                    # Connect ik roll joint's rotation to roll joint's rotation to detail controls to roll controls

                    for index in range(LEN_DETAILS):
                        roll_jnt = roll.joints[f"{g.name}{index}"]
                        roll_root = roll.joints[f"{g.name}{0}"]
                        roll_end = roll.joints[f"{g.name}{LEN_INDEX}"]
                        roll_ctrl = roll.controls[f"{g.name}{ROLL}{index}"]
                        detail_ctrl = roll.controls[f"{g.name}{DETAIL}{index}"]
                        ratio = index / LEN_INDEX if LEN_INDEX != 0 else 0

                        if index == LEN_INDEX:
                            cmds.pointConstraint(roll_handle_ik_driver, roll_jnt)

                        # Connect translate
                        if 0 < index < LEN_INDEX:
                            pos_node_name = limb_node_format(
                                PROJECT, IK, side, g.name, f"{MULT_DIV}_{ROLL}_pos", f"0{index}"
                            )
                            pos_node = cmds.createNode("multDoubleLinear", n=pos_node_name)
                            cmds.setAttr(f"{pos_node}.input1", ratio)
                            cmds.connectAttr(f"{roll_end}.translate{axis}", f"{pos_node}.input2")
                            cmds.connectAttr(f"{pos_node}.output", f"{roll_jnt}.translate{axis}")

                        # Connect Rotation
                        if index < LEN_INDEX:
                            rot_node_name = limb_node_format(
                                PROJECT, IK, side, g.name, f"{MULT_DIV}_{ROLL}_orient", f"0{index}"
                            )
                            rot_node = cmds.createNode("multDoubleLinear", n=rot_node_name)
                            cmds.setAttr(f"{rot_node}.input1", ratio - 1)
                            cmds.connectAttr(f"{roll_ik_root}.rotate{axis}", f"{rot_node}.input2")
                            cmds.connectAttr(f"{rot_node}.output", f"{roll_jnt}.rotate{axis}")

                        # Connect joint to control
                        cmds.parentConstraint(roll_jnt, detail_ctrl.top)

                        # Connect control detail to roll
                        cmds.parentConstraint(detail_ctrl.ctrl, roll_ctrl.ctrl)
