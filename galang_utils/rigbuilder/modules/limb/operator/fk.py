from maya import cmds
from galang_utils.rigbuilder.modules.limb.component.zcomponent import LimbComponent


class LimbFKOperator:
    def __init__(self, component: LimbComponent):
        self.component = component
        self.joints = component.fk.joints
        self.controls = component.fk.controls

    def run(self):
        for jnt, ctrl in zip(self.joints, self.controls):
            cmds.parentConstraint(ctrl, jnt)
            cmds.scaleConstraint(ctrl, jnt, mo=True)
