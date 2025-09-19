from maya import cmds
from rig_x_frame.constants.project import role as role

from rig_x_frame.mod_zero.base.component.setup_group import GroupComponent
from rig_x_frame.mod_zero.base.component.zcomponents import Components


class GroupOperator:
    def __init__(self, component: Components):
        self.component = component

    def run(self):
        guides = self.component.module.guides
        side = self.component.module.guide.side

        # Pre Compute DAG objects
        rig = self.component.group.rig
        dnt = self.component.group.dnt
        constraint = self.component.group.constraint
        fk = self.component.fk.group
        fk_joints = self.component.fk.joints.group

        # STEP 0 : PARENT PRE COMPUTED GROUPS
        cmds.parent(fk, rig)
        cmds.parent(fk_joints, dnt)

        # STEP 1 : PARENT CONSTRAINT NODES TO CONSTRAINT BUFFER
        constraint_nodes = cmds.ls("*Constraint1")
        for node in constraint_nodes:
            side_match = side in node
            guide_match = any(guide.name_raw in node for guide in guides)
            if side_match and guide_match:
                cmds.parent(node, constraint)
