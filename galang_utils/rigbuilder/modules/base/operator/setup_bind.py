from maya import cmds
from rigbuilder.modules.base.component.setup_bind import BindComponent
from rigbuilder.modules.base.component.zcomponents import Components


class BindOperator:
    def __init__(self, components: Components):
        self.components = components

    def run(self):
        joints = self.components.bind.joints
        drivers = self.components.fk.joints
        for joint, driver in zip(joints, drivers):
            cmds.parentConstraint(driver, joint)
            cmds.scaleConstraint(driver, joint)
