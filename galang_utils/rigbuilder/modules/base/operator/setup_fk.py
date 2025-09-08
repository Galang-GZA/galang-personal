from maya import cmds

from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup

from rigbuilder.modules.base.component.setup_fk import FKComponent
from rigbuilder.modules.base.component.zcomponents import Components


class FKOperator(FKComponent):
    def __init__(self, component: Components):
        super().__init__(component.module)

    def run(self):
        for joint, control in zip(self.joints, self.controls):
            cmds.parentConstraint(control, joint)
