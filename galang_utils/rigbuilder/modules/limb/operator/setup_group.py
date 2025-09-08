from maya import cmds
from rigbuilder.constants.project import role as role

from rigbuilder.modules.base.operator.setup_group import GroupOperator
from rigbuilder.modules.limb.component.zcomponents import LimbComponents


class LimbGroupOperator(GroupOperator):
    def __init__(self, components: LimbComponents):
        super().__init__(components.module)

        # Pre-computed rig components group
        self.ik = components.ik.group
        self.result = components.result.group
        self.detail = components.detail.group
        self.setting = components.setting.group

        # Pre-computed dnt components group
        self.ik_joint = components.ik.joints.group
        self.upper_detail_joints = components.detail.upper.joints.group
        self.lower_detail_joints = components.detail.lower.joints.group

    def run(self):
        # STEP 0 : PARENT PRE COMPUTED GROUPS
        # Rig components group
        rig_components_group = [self.fk, self.ik, self.result, self.detail, self.setting]
        for group in rig_components_group:
            cmds.parent(group, self.rig)

        dnt_components_group = [self.fk_joints, self.ik_joint, self.upper_detail_joints, self.lower_detail_joints]
        for group in dnt_components_group:
            cmds.parent(group, self.dnt)

        # STEP 1 : PARENT CONSTRAINT NODES TO CONSTRAINT BUFFER
        constraint_nodes = cmds.ls("*Constraint1")
        for node in constraint_nodes:
            side_match = self.side in node
            guide_match = any(guide.name_raw in node for guide in self.guides)
            if side_match and guide_match:
                cmds.parent(node, self.constraint)
