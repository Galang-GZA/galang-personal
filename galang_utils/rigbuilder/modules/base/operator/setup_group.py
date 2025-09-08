from maya import cmds
from rigbuilder.constants.project import role as role

from rigbuilder.modules.base.component.setup_group import GroupComponent
from rigbuilder.modules.base.component.zcomponents import Components


class GroupOperator(GroupComponent):
    def __init__(self, component: Components):
        super().__init__(component.module)
        self.component = component
        self.guides = component.module.guides
        self.side = component.module.guide.side

        # Pre Compute DAG objects
        self.fk = component.fk.group
        self.fk_joints = component.fk.joints.group

    def run(self):
        # STEP 0 : PARENT PRE COMPUTED GROUPS
        cmds.parent(self.fk, self.rig)
        cmds.parent(self.fk_joints, self.dnt)

        # STEP 1 : PARENT CONSTRAINT NODES TO CONSTRAINT BUFFER
        constraint_nodes = cmds.ls("*Constraint1")
        for node in constraint_nodes:
            side_match = self.side in node
            guide_match = any(guide.name_raw in node for guide in self.guides)
            if side_match and guide_match:
                cmds.parent(node, self.constraint)
