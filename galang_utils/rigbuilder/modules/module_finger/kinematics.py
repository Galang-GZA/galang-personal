"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_finger.constant import *
from galang_utils.rigbuilder.modules.module_finger.guide import Finger_GuideInfo, Finger_GuideList
from galang_utils.rigbuilder.modules.module_finger.controls import Finger_ControlCreator
from galang_utils.rigbuilder.modules.module_finger.jointchain import Finger_JointChainSetup


class Finger_FKSetup:
    def __init__(self, guide):
        self.guide = Finger_GuideInfo(guide)
        self.input = Finger_GuideList(guide)
        self.fk_joint_chain = Finger_JointChainSetup(guide, NK)
        self.fk_module_group = None
        self.fk_module_map = {}

    def build(self):
        # Step 0: Create NK Module Group
        group_name = finger_level_format(PROJECT, NK, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.fk_module_group = cmds.group(em=True, name=group_name)
            cmds.xform(self.fk_module_group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # Step 1: Create NK Joint Chain
        self.fk_joint_chain.build()
        cmds.parent(self.fk_joint_chain.group, self.fk_module_group)

        # Step 2: Create NK Controls
        for g in self.input.guides:
            if g.is_guide_end or g.is_guide_misc:
                continue
            fk_control = Finger_ControlCreator(g.name, NK)
            fk_control.create()
            fk_joint = self.fk_joint_chain.joints_created.get(g.name)
            self.fk_module_map[g.name] = {CTRL: fk_control, JNT: fk_joint}

        # Step 3: Setup Module hierarchy
        for g in self.input.guides:
            if g.is_guide_end or g.is_guide_misc:
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


class Finger_IKSetup:
    def __init__(self, guide):
        self.guide = Finger_GuideInfo(guide)
        self.input = Finger_GuideList(guide)
        self.ik_joint_chain = Finger_JointChainSetup(guide, IK)
        self.ik_module_group = None
        self.ik_module_map = {}
        self.ik_handle = None

    def build(self):
        # Step 0: Create IK Module Group
        group_name = finger_level_format(PROJECT, IK, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.ik_module_group = cmds.group(em=True, name=group_name)
            cmds.xform(self.ik_module_group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # Step 1: Create IK Joint Chain
        self.ik_joint_chain.build()
        cmds.parent(self.ik_joint_chain.group, self.ik_module_group)

        # Step 2: Define Start & End Joints, Create Contrtols, Parent to Main Group
        start_ik_joint = None
        mid_ik_joint = None
        end_ik_joint = None
        pv_guide_joint = None
        start_ik_control = None
        pole_vector_control = None
        end_ik_control = None
        finger_name = None

        for g in self.input.guides:
            jnt = self.ik_joint_chain.joints_created.get(g.name)
            if g.is_guide_end or g.is_guide_misc:
                continue
            if g.module == LIMB:
                start_ik_joint = jnt
                start_ik_control = Finger_ControlCreator(g.name, IK)
                start_ik_control.create()
                self.ik_module_map[g.name] = {JNT: start_ik_joint, CTRL: start_ik_control}
                cmds.parent(start_ik_control.top, self.ik_module_group)
                cmds.pointConstraint(start_ik_control.ctrl, start_ik_joint)
                cmds.scaleConstraint(start_ik_control.ctrl, start_ik_joint, mo=1)

                # Create local control
                start_ik_control_local = Finger_ControlCreator(g.name, IK)
                start_ik_control_local.create()
                # print(f"Created Pole Vector: {pole_vector_control.ctrl} at {g.[position]}") #For Debugging

            elif g.module == HINGES:
                mid_ik_joint = jnt
                hinges_guide_children = cmds.listRelatives(g.name, c=True)
                for c in hinges_guide_children:
                    c_info = Finger_GuideInfo(c)
                    if c_info.is_guide_misc:
                        pv_guide_joint = c
                pole_vector_control = Finger_ControlCreator(pv_guide_joint, IK)
                pole_vector_control.create()
                self.ik_module_map[g.name] = {JNT: mid_ik_joint, CTRL: pole_vector_control}
                cmds.parent(pole_vector_control.top, self.ik_module_group)
                # cmds.scaleConstraint(pole_vector_control.ctrl, mid_ik_joint)

                # Lock and Hide attributes
                attrs = ["rx", "ry", "rz"]
                for attr in attrs:
                    cmds.setAttr(f"{pole_vector_control.ctrl}.{attr}", lock=True, keyable=False, channelBox=False)

            elif g.module in {HAND, FOOT}:
                finger_name = g.name_raw
                end_ik_joint = jnt
                end_ik_control = Finger_ControlCreator(g.name, IK)
                end_ik_control.create()
                self.ik_module_map[g.name] = {JNT: end_ik_joint, CTRL: end_ik_control}
                cmds.parent(end_ik_control.top, self.ik_module_group)
                cmds.scaleConstraint(end_ik_control.ctrl, end_ik_joint, mo=1)

        # cmds.scaleConstraint(start_ik_control.ctrl, end_ik_control.ctrl, mid_ik_joint, mo=1)

        if not start_ik_joint or not end_ik_joint:
            cmds.error("Ay, cant make ik here lha")

        # Step 3: Create IK Handle
        ik_handle_name = finger_level_format(PROJECT, IK, self.guide.side, finger_name, level=None)
        ik_solver_name = finger_level_format(PROJECT, IK, self.guide.side, finger_name, level=None, item="RPsolver")
        self.ik_handle = cmds.ikHandle(
            n=ik_handle_name,
            sj=start_ik_joint,
            ee=end_ik_joint,
            sol="ikRPsolver",
        )[0]
        cmds.rename("effector1", ik_solver_name)

        # Step 4: Parent the IK Handle to the End Control
        if end_ik_control:
            cmds.parent(self.ik_handle, end_ik_control.ctrl)
        else:
            cmds.parent(self.ik_handle, self.ik_module_group)

        # Step 5: Pole Vector Constraint
        if pole_vector_control:
            cmds.poleVectorConstraint(pole_vector_control.ctrl, self.ik_handle)
