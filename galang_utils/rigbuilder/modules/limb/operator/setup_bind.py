from maya import cmds
from typing import Dict, Union

from rigbuilder.constants.general import role as gen_role
from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup
from rigbuilder.modules.limb.component.setup_bind import LimbBindComponent
from rigbuilder.modules.limb.component.zcomponents import LimbComponents


class LimbBindOperator(LimbBindComponent):
    def __init__(self, component: LimbComponents):
        super().__init__(component)

        # Pre compute dag components
        self.drivers = component.bind_driver
        self.upper_sub_driver = component.detail.upper.joints
        self.lower_sub_driver = component.detail.lower.joints

    def run(self):
        # STEP 0 : CONNECT PRE COMPUTED DAG COMPONENTS
        # Constraint bind drivers to bind joint
        for joint, driver in zip(self.joints, self.drivers):
            cmds.parentConstraint(driver, joint)
            cmds.scaleConstraint(driver, joint)

        # Constraint sub drivers to sub bind joints
        sub_drivers = [self.lower_sub_driver, self.upper_sub_driver]
        sub_joints = [self.lower_sub_joints, self.upper_sub_joints]
        for i in range(2):
            for joint, driver in zip(sub_drivers[i], sub_joints[i]):
                cmds.parentConstraint(driver, joint)
                cmds.scaleConstraint(driver, joint)
