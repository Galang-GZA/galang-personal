from maya import cmds

from rig_x_frame.constants.project import role as role
from rig_x_frame.constants.project import setup as setup
from rig_x_frame.mod_zero.limb.component.zcomponents import LimbComponents


class LimbBindOperator:
    def __init__(self, component: LimbComponents):
        # Pre computed dag components
        self.joints = component.bind.joints
        self.lower_sub_joints = component.bind.lower_sub_joints
        self.upper_sub_joints = component.bind.upper_sub_joints

        self.drivers = component.result.joints
        self.upper_sub_driver = component.detail.upper.result_joints
        self.lower_sub_driver = component.detail.lower.result_joints

    def run(self):
        self.__connect_bind_drivers_to_bind_joints()
        self.__connect_sub_driver_to_sub_joints()

    def __connect_bind_drivers_to_bind_joints(self):
        # Constraint bind drivers to bind joint
        for joint, driver in zip(self.joints, self.drivers):
            cmds.parentConstraint(driver, joint)
            cmds.scaleConstraint(driver, joint)

    def __connect_sub_driver_to_sub_joints(self):
        # Constraint sub drivers to sub bind joints
        sub_drivers = [self.lower_sub_driver, self.upper_sub_driver]
        sub_joints = [self.lower_sub_joints, self.upper_sub_joints]
        for i in range(2):
            for joint, driver in zip(sub_drivers[i], sub_joints[i]):
                cmds.parentConstraint(driver, joint)
                cmds.scaleConstraint(driver, joint)
