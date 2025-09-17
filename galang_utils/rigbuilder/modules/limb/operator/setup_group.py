from maya import cmds
from rigbuilder.constants.project import role as role

from rigbuilder.modules.base.operator.setup_group import GroupOperator
from rigbuilder.modules.limb.component.zcomponents import LimbComponents


class LimbGroupOperator:
    def __init__(self, components: LimbComponents):
        self.components = components

    def run(self):
        side = self.components.module.side
        guides = self.components.module.guides
        # Pre-computed rig self.components group
        rig = self.components.group.rig
        dnt = self.components.group.dnt
        constraint = self.components.group.constraint

        fk = self.components.fk.group
        ik = self.components.ik.group
        result = self.components.result.group
        detail = self.components.detail.group
        setting = self.components.setting.group

        # Pre-computed dnt self.components group
        fk_joint = self.components.fk.joints.group
        ik_joint = self.components.ik.joints.group
        upper_detail_joints = self.components.detail.upper.result_joints.group
        lower_detail_joints = self.components.detail.lower.result_joints.group

        # STEP 0 : PARENT PRE COMPUTED GROUPS
        # Rig self.components group
        rig_components_group = [fk, ik, result, detail, setting]
        for group in rig_components_group:
            cmds.parent(group, rig)

        dnt_components_group = [fk_joint, ik_joint, upper_detail_joints, lower_detail_joints]
        for group in dnt_components_group:
            cmds.parent(group, dnt)

        # STEP 1 : PARENT CONSTRAINT NODES TO CONSTRAINT BUFFER
        constraint_nodes = cmds.ls("*Constraint1")
        for node in constraint_nodes:
            side_match = side in node
            guide_match = any(guide.name_raw in node for guide in guides)
            if side_match and guide_match:
                cmds.parent(node, constraint)
