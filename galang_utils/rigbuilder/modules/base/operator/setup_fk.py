from maya import cmds
from typing import List

from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup
from rigbuilder.constants.general import role as gen_role

from rigbuilder.modules.base.component.zcomponent import Component
from rigbuilder.modules.base.operator.dg import Node
from rigbuilder.modules.base.operator.distance import DistanceNode, DistanceSet


class FKOperator:
    def __init__(self, component: Component):
        # Pre compute dag components
        self.joints = component.fk.joints
        self.controls = component.fk.controls

    def run(self):
        for joint, control in zip(self.joints, self.controls):
            cmds.parentConstraint(control, joint)
