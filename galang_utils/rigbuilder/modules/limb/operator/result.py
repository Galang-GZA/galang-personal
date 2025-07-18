from maya import cmds
from galang_utils.rigbuilder.modules.limb.component.zcomponent import LimbComponent


class LimbResultOperator:
    def __init__(self, component: LimbComponent):
        self.module = component.result.module
        self.guides = component.result.module.guides
        self.ik_joints = component.ik.joints
        self.fk_joints = component.fk.joints
        self.result_joints = component.result.joints
        self.pair_blends = component.result.pair_blends
        self.scale_blends = component.result.scale_blends


    def run(self):
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
