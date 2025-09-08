from maya import cmds

from rigbuilder.constants.project import role as role
from rigbuilder.modules.base.operator.dg import NodeSet
from rigbuilder.modules.limb.component.setup_result import LimbResultComponent
from rigbuilder.modules.limb.component.zcomponents import LimbComponents


class LimbResultOperator(LimbResultComponent):
    def __init__(self, components: LimbComponents):
        super().__init__(module)
        module = components.module

        # Pre computed dag components
        self.ik_joints = components.ik.joints
        self.fk_joints = components.fk.joints
        self.result_joints = components.result.joints
        self.setting_control = components.setting.control

        # Pre compute dg nodes
        self.pair_blends = NodeSet(self.guides, module, [role.RESULT, role.PAIRBLEND])
        self.scale_blends = NodeSet(self.guides, module, [role.RESULT, role.BLENDCOLORS])

    def run(self):
        # STEP 0 : CREATE PRE COMPUTED DG NODES
        self.pair_blends.create()
        self.scale_blends.create()

        # STEP 1 : CONNECT DG NODES TO DAG COMPONENTS TO RESULT JOINTS
        # Ik joint and fk joint - blend nodes - result joints
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

        # STEP 2 : CONNECT IK FK JOINTS TO RESULT
        # Connect with constraint
        kinematics_switch_attr = f"{self.setting_control}.{role.IKFKSWITCH}"
        for i in range(len(self.guides)):
            cmds.connectAttr(kinematics_switch_attr, f"{self.pair_blends[i]}.weight", force=True)
            cmds.connectAttr(kinematics_switch_attr, f"{self.scale_blends[i]}.blender", force=True)
