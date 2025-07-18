from maya import cmds
from galang_utils.rigbuilder.constant.project import role as TASK_ROLE
from galang_utils.rigbuilder.modules.limb.component.zcomponent import LimbComponent


class LimbGroupOperator:
    def __init__(self, component: LimbComponent):
        self.component = component
        self.guides = component.container.module.guides
        self.side = component.container.module.guide.side

    def run(self):
        grp_system = self.component.container.groups[TASK_ROLE.SYSTEM]
        grp_stasis = self.component.container.groups[TASK_ROLE.STASIS]
        grp_constraint = self.component.container.groups[TASK_ROLE.CONSTRAINT]

        grp_ik = self.component.ik.groups
        grp_fk = self.component.fk.groups
        grp_result = self.component.result.groups
        grp_roll = self.component.sub.groups
        grp_setting = self.component.setting.setting.top

        # Step 1 : Parent constraint nodes to their group
        constraint_nodes = cmds.ls("*Constraint1")
        for node in constraint_nodes:
            if self.side in node:
                if any(g.name_raw in node for g in self.guides):
                    cmds.parent(node, grp_constraint)

        # Step 2 : Parent stasis components to their group
        grps_stasis = [grp_ik[TASK_ROLE.JNT], grp_fk[TASK_ROLE.JNT], grp_ik[TASK_ROLE.LOCATOR], grp_ik[TASK_ROLE.DISTANCE], grp_constraint]
        for grp in grps_stasis:
            cmds.parent(grp, grp_stasis)

        # Step 3 : Parent system components to their group
        grps_sys = [grp_ik[TASK_ROLE.MASTER], grp_fk[TASK_ROLE.MASTER], grp_roll[TASK_ROLE.MASTER], grp_result, grp_setting]
        for grp in grps_sys:
            cmds.parent(grp, grp_system)

        # Step 4 : Parent roll components to system group
