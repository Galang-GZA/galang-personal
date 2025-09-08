from maya import cmds
from rigbuilder.modules.base.component.setup_bind import BindComponent
from rigbuilder.modules.base.component.zcomponents import Components


class BindOperator(BindComponent):
    def __init__(self, component: Components):
        super().__init__(component.module)

        # Pre compute dag components
        self.drivers = component.bind_driver

    def run(self):
        for joint, driver in zip(self.joints, self.drivers):
            cmds.parentConstraint(driver, joint)
            cmds.scaleConstraint(driver, joint)
