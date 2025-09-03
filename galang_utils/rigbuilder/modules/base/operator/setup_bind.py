from maya import cmds
from rigbuilder.modules.base.component.zcomponent import Component


class BindOperator:
    def __init__(self, component: Component):
        self.module = component.module

        # Pre compute dag components
        self.joints = component.bind.joints
        self.drivers = component.bind_driver

    def run(self):
        for joint, driver in zip(self.joints, self.drivers):
            cmds.parentConstraint(driver, joint)
            cmds.scaleConstraint(driver, joint)
