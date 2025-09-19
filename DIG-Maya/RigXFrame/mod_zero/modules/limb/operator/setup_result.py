from maya import cmds

from rig_x_frame.constants.project import role as role
from rig_x_frame.mod_zero.base.operator.dg import NodeSet
from rig_x_frame.mod_zero.limb.component.setup_result import LimbResultComponent
from rig_x_frame.mod_zero.limb.component.zcomponents import LimbComponents

"""GA USYAH SUPER SUPER KE COMPONENT, NGE INIT LAGI ITUH"""


class LimbResultOperator:
    def __init__(self, components: LimbComponents):
        self.module = components.module
        self.guides = components.module.guides

        # Pre computed dag components
        self.ik_joints = components.ik.joints
        self.fk_joints = components.fk.joints
        self.result_joints = components.result.joints
        self.setting_control = components.setting.control

    def run(self):
        self.__create_dg_nodes()
        self.__connect_kinematics_to_dg_to_result()
        self.__connect_settings_to_dg

    def __create_dg_nodes(self):
        self.pair_blends = NodeSet(self.guides, self.module, [role.RESULT, role.PAIRBLEND])
        self.scale_blends = NodeSet(self.guides, self.module, [role.RESULT, role.BLENDCOLORS])
        dg_nodes = [self.pair_blends, self.scale_blends]
        for node in dg_nodes:
            node.run()

    def __connect_kinematics_to_dg_to_result(self):
        # Direct connect kinematics component to dg nodes to result
        for i in range(len(self.guides)):
            connections = [
                (self.ik_joints[i], "translate", self.pair_blends[i], "inTranslate1"),
                (self.ik_joints[i], "rotate", self.pair_blends[i], "inRotate1"),
                (self.ik_joints[i], "scale", self.scale_blends[i], "color2"),
                (self.fk_joints[i], "translate", self.pair_blends[i], "inTranslate2"),
                (self.fk_joints[i], "rotate", self.pair_blends[i], "inRotate2"),
                (self.fk_joints[i], "scale", self.scale_blends[i], "color1"),
                (self.pair_blends[i], "outTranslate", self.result_joints[i], "translate"),
                (self.pair_blends[i], "outRotate", self.result_joints[i], "rotate"),
                (self.scale_blends[i], "output", self.result_joints[i], "scale"),
            ]
            for scr_node, scr_attr, dst_node, dst_attr in connections:
                cmds.connectAttr(f"{scr_node}.{scr_attr}", f"{dst_node}.{dst_attr}")

            cmds.setAttr(f"{self.pair_blends[i]}.weight", 0.5)

    def __connect_settings_to_dg(self):
        # Connect IK FK joints to result joints with constraint
        kinematics_switch_attr = f"{self.setting_control}.{role.IKFKSWITCH}"
        for i in range(len(self.guides)):
            cmds.connectAttr(kinematics_switch_attr, f"{self.pair_blends[i]}.weight", force=True)
            cmds.connectAttr(kinematics_switch_attr, f"{self.scale_blends[i]}.blender", force=True)
