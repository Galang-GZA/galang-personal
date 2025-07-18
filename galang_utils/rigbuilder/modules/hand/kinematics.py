"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from galang_utils.rigbuilder.constant.constant_general import *
from galang_utils.rigbuilder.constant.constant_project import *
from galang_utils.rigbuilder.modules.hand.constant import *
from galang_utils.rigbuilder.modules.hand.guide import Hand_GuideInfo, Hand_GuideList
from galang_utils.rigbuilder.modules.hand.controls import Hand_ControlCreator
from galang_utils.rigbuilder.modules.hand.jointchain import Hand_JointChainSetup


class Hand_FKSetup:
    def __init__(self, guide, kinematics):
        self.guide = Hand_GuideInfo(guide)
        self.input = Hand_GuideList(guide)
        self.kinematics = kinematics
        self.fk_joint_chain = Hand_JointChainSetup(guide, self.kinematics)
        self.fk_module_group = None
        self.fk_module_map = {}

    def build(self):
        # Step 0: Create FK Module Group
        group_name = hand_level_format(PROJECT, self.kinematics, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.fk_module_group = cmds.group(em=True, name=group_name)
            cmds.xform(self.fk_module_group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # Step 1: Create FK Joint Chain
        self.fk_joint_chain.build()
        cmds.parent(self.fk_joint_chain.group, self.fk_module_group)

        # Step 2: Create FK Controls
        for g in self.input.guides:
            if g.is_guide_end or g.is_guide_misc:
                continue

            if not g.module == ROOT:
                module_contents: Dict = MODULE_MAP.get(self.guide.module, {}).get("contents", [])
                if g.module not in module_contents:
                    continue

            fk_control = Hand_ControlCreator(g.name, NK)
            fk_control.create()
            fk_joint = self.fk_joint_chain.joints_created.get(g.name)
            self.fk_module_map[g.name] = {CTRL: fk_control, JNT: fk_joint}

        # Step 3: Setup Module hierarchy
        for g in self.input.guides:
            if g.is_guide_end or g.is_guide_misc:
                continue

            if not g.module == ROOT:
                module_contents: Dict = MODULE_MAP.get(self.guide.module, {}).get("contents", [])
                if g.module not in module_contents:
                    continue

            top_node = self.fk_module_map[g.name][CTRL].top
            parent_entry = self.fk_module_map.get(g.parent)
            if parent_entry:
                parent_ctrl = self.fk_module_map[g.parent][CTRL].ctrl
                cmds.parent(top_node, parent_ctrl)
            else:
                cmds.parent(top_node, self.fk_module_group)

        # step 4: Parent Constraint the control to joint
        for g in self.input.guides:
            if g.is_guide_end or g.is_guide_misc:
                continue

            if not g.module == ROOT:
                module_contents: Dict = MODULE_MAP.get(self.guide.module, {}).get("contents", [])
                if g.module not in module_contents:
                    continue

            fk_control = self.fk_module_map[g.name][CTRL].ctrl
            fk_joint = self.fk_module_map[g.name][JNT]
            if fk_control and fk_joint:
                existing_constraint = cmds.listRelatives(fk_joint, typ="constraint", f=True) or []
                for c in existing_constraint:
                    cmds.delete(c)
                cmds.parentConstraint(fk_control, fk_joint, mo=1)
                cmds.scaleConstraint(fk_control, fk_joint, mo=1)
            else:
                cmds.warning(f"Missing control or joint for {g.name}, constrain skippzzz")
