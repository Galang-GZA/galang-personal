from maya import cmds

from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup

from rigbuilder.modules.base.component.setup_fk import FKComponent
from rigbuilder.modules.base.component.zcomponents import Components


class FKOperator:
    def __init__(self, components: Components):
        self.components = components

    def run(self):
        joints = self.components.fk.joints
        controls = self.components.fk.controls

        for joint, control in zip(joints, controls):
            cmds.parentConstraint(control, joint)
