"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from galang_utils.rigbuilder.guide import *
from galang_utils.rigbuilder.constant import *
from galang_utils.rigbuilder.controls import *


class JointChainSetup:
    def __init__(self, guide, kinematics):
        self.guide = GuideInfo(guide)
        self.input = GuideList(guide)
        self.joints_created = {}
        self.kinematics = kinematics
        self.group = None

    def build(self):
        group_name = level_format(self.kinematics, self.guide.side, self.guide.name_raw, GROUP, JNT)
        if not cmds.objExists(group_name):
            self.group = cmds.group(empty=True, name=group_name)
            cmds.xform(self.group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")
        cmds.hide(self.group)

        for g in self.input.guides:
            if g.is_guide_end or g.is_guide_misc:
                continue

            # if g.module_start:
            #     joint_name = joint_format(self.kinematics, g.side, g.parent)
            # else:
            #     joint_name = joint_format(self.kinematics, g.side, g.name_raw)
            joint_name = joint_format(self.kinematics, g.side, g.name_raw)
            if cmds.objExists(joint_name):
                cmds.warning(f"{joint_name} is already created. Skipppz")
                continue

            cmds.select(clear=True)
            jnt = cmds.joint(
                name=joint_format(self.kinematics, g.side, g.name_raw),
                position=g.position,
                orientation=g.orientation,
            )
            cmds.setAttr(f"{jnt}.type", g.module_id)
            cmds.setAttr(f"{jnt}.side", g.side_id)
            self.joints_created[g.name] = jnt
            if g.name_raw == self.guide.name_raw:
                cmds.parent(jnt, self.group)
            # print(f"Created joint: {jnt}")

        for g in self.input.guides:
            if g.parent:
                child = self.joints_created.get(g.name)
                parent = self.joints_created.get(g.parent)
                if child and parent:
                    cmds.parent(child, parent)


class BindSetup:
    def __init__(self, guide):
        self.bind_joint_chain = JointChainSetup(guide, BIND)

    def build(self):
        self.bind_joint_chain.build()


class FKSetup:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.input = GuideList(guide)
        self.fk_joint_chain = JointChainSetup(guide, FK)
        self.fk_module_group = None
        self.fk_module_map = {}

    def build(self):
        # Step 0: Create FK Module Group
        group_name = level_format(FK, self.guide.side, self.guide.name_raw, GROUP)
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
            fk_control = ControlCreator(g.name, FK)
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


class IKSetup:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.input = GuideList(guide)
        self.ik_joint_chain = JointChainSetup(guide, IK)
        self.ik_module_group = None
        self.ik_module_map = {}
        self.ik_handle = None

    def build(self):
        # Step 0: Create IK Module Group
        group_name = level_format(IK, self.guide.side, self.guide.name_raw, GROUP)
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
        limb_name = None

        for g in self.input.guides:
            jnt = self.ik_joint_chain.joints_created.get(g.name)
            if g.is_guide_end or g.is_guide_misc:
                continue
            if g.module == LIMB:
                start_ik_joint = jnt
                start_ik_control = ControlCreator(g.name, IK)
                start_ik_control.create()
                self.ik_module_map[g.name] = {JNT: start_ik_joint, CTRL: start_ik_control}
                cmds.parent(start_ik_control.top, self.ik_module_group)
                cmds.pointConstraint(start_ik_control.ctrl, start_ik_joint)
                cmds.scaleConstraint(start_ik_control.ctrl, start_ik_joint, mo=1)
                # print(f"Created Pole Vector: {pole_vector_control.ctrl} at {g.[position]}") #For Debugging

            elif g.module == HINGES:
                mid_ik_joint = jnt
                hinges_guide_children = cmds.listRelatives(g.name, c=True)
                for c in hinges_guide_children:
                    c_info = GuideInfo(c)
                    if c_info.is_guide_misc:
                        pv_guide_joint = c
                pole_vector_control = ControlCreator(pv_guide_joint, IK)
                pole_vector_control.create()
                self.ik_module_map[g.name] = {JNT: mid_ik_joint, CTRL: pole_vector_control}
                cmds.parent(pole_vector_control.top, self.ik_module_group)
                cmds.scaleConstraint(pole_vector_control.ctrl, mid_ik_joint)

                # Lock and Hide attributes
                attrs = ["rx", "ry", "rz"]
                for attr in attrs:
                    cmds.setAttr(f"{pole_vector_control.ctrl}.{attr}", lock=True, keyable=False, channelBox=False)

            elif g.module in {HAND, FOOT}:
                limb_name = g.name_raw
                end_ik_joint = jnt
                end_ik_control = ControlCreator(g.name, IK)
                end_ik_control.create()
                self.ik_module_map[g.name] = {JNT: end_ik_joint, CTRL: end_ik_control}
                cmds.parent(end_ik_control.top, self.ik_module_group)
                cmds.scaleConstraint(end_ik_control.ctrl, end_ik_joint, mo=1)

        # cmds.scaleConstraint(start_ik_control.ctrl, end_ik_control.ctrl, mid_ik_joint, mo=1)

        if not start_ik_joint or not end_ik_joint:
            cmds.error("Ay, cant make ik here lha")

        # Step 3: Create IK Handle
        ik_handle_name = level_format(IK, self.guide.side, limb_name, level=None)
        ik_solver_name = level_format(IK, self.guide.side, limb_name, level=None, item="RPsolver")
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


class ModuleLimb:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.input = GuideList(guide)
        self.result_joint = JointChainSetup(guide, RESULT)
        self.fk = FKSetup(guide)
        self.ik = IKSetup(guide)
        self.limb_module_group = None
        self.limb_module_blend_map = {}
        self.limb_module_control = None

    def build(self):
        # Step 0: Create Module Group
        group_name = level_format(self.guide.module, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.limb_module_group = cmds.group(em=True, name=group_name)
            cmds.xform(self.limb_module_group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # Step 1: Build FK, IK, and Result Joint Chain
        self.fk.build()
        self.ik.build()
        self.result_joint.build()

        # Step 2: Put Items in Module Group
        cmds.parent(self.ik.ik_module_group, self.limb_module_group)
        cmds.parent(self.fk.fk_module_group, self.limb_module_group)
        cmds.parent(self.result_joint.group, self.limb_module_group)

        # Step 3: Create module control and connect FK, IK to Result Joints
        kinematic_switch_attr = None
        kinematic_switch_reverse = None
        controls = None

        for g in self.input.guides:
            if g.is_guide_end or g.is_guide_misc:
                continue

            result_joint = self.result_joint.joints_created[g.name]
            ik_data = self.ik.ik_module_map.get(g.name)
            fk_data = self.fk.fk_module_map.get(g.name)

            # Create module control
            if g.module in (HAND, FOOT):
                self.limb_module_control = ControlCreator(g.name, MODULE)
                self.limb_module_control.create()

                # Lock and hide oiriginal attributes
                attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "visibility"]
                for attr in attrs:
                    cmds.setAttr(f"{self.limb_module_control.ctrl}.{attr}", lock=True, keyable=False, channelBox=False)

                # Create kinematic switch attribute
                if not cmds.attributeQuery(IKFKSWITCH, node=self.limb_module_control.ctrl, exists=True):
                    cmds.addAttr(
                        self.limb_module_control.ctrl, ln=IKFKSWITCH, at="double", min=0, max=1, dv=0, keyable=True
                    )
                    cmds.parent(self.limb_module_control.top, self.limb_module_group)
                    cmds.pointConstraint(result_joint, self.limb_module_control.top)
                    # cmds.scaleConstraint(result_joint, self.limb_module_control.top)

                kinematic_switch_attr = f"{self.limb_module_control.ctrl}.{IKFKSWITCH}"
                kinematic_switch_reverse = cmds.createNode(
                    "reverse", name=level_format(MODULE, g.side, g.name_raw, level=None, item=REVERSE)
                )
                cmds.connectAttr(kinematic_switch_attr, f"{kinematic_switch_reverse}.inputX")
                cmds.connectAttr(kinematic_switch_attr, f"{self.fk.fk_module_group}.visibility")
                cmds.connectAttr(f"{kinematic_switch_reverse}.outputX", f"{self.ik.ik_module_group}.visibility")

            if not (result_joint and ik_data and fk_data):
                continue
            ik_joint = ik_data[JNT]
            fk_joint = fk_data[JNT]
            pairblend_name = level_format(RESULT, g.side, g.name_raw, level=None, item=PAIRBLEND)
            blendcolor_name = level_format(RESULT, g.side, g.name_raw, level=None, item=SCALEBLEND)
            pair_blend = cmds.createNode("pairBlend", name=pairblend_name)
            scale_blend = cmds.createNode("blendColors", name=blendcolor_name)

            cmds.connectAttr(f"{ik_joint}.translate", f"{pair_blend}.inTranslate1")
            cmds.connectAttr(f"{ik_joint}.rotate", f"{pair_blend}.inRotate1")
            cmds.connectAttr(f"{ik_joint}.scale", f"{scale_blend}.color2")

            cmds.connectAttr(f"{fk_joint}.translate", f"{pair_blend}.inTranslate2")
            cmds.connectAttr(f"{fk_joint}.rotate", f"{pair_blend}.inRotate2")
            cmds.connectAttr(f"{fk_joint}.scale", f"{scale_blend}.color1")

            cmds.connectAttr(f"{pair_blend}.outTranslate", f"{result_joint}.translate")
            cmds.connectAttr(f"{pair_blend}.outRotate", f"{result_joint}.rotate")
            cmds.connectAttr(f"{scale_blend}.output", f"{result_joint}.scale")

            cmds.setAttr(f"{pair_blend}.weight", 0.5)

            self.limb_module_blend_map[g.name] = {PAIRBLEND: pair_blend, SCALEBLEND: scale_blend}

        # Step 4: Connect module control to Ik & Fk
        for g in self.input.guides:
            if g.is_guide_end or g.is_guide_misc:
                continue

            # Translation blend
            pair_blend = self.limb_module_blend_map[g.name][PAIRBLEND]
            scale_blend = self.limb_module_blend_map[g.name][SCALEBLEND]
            cmds.connectAttr(kinematic_switch_attr, f"{pair_blend}.weight", force=True)
            cmds.connectAttr(kinematic_switch_attr, f"{scale_blend}.blender", force=True)

            # Attribute proxy
            ik_control = self.ik.ik_module_map.get(g.name)[CTRL]
            fk_control = self.fk.fk_module_map.get(g.name)[CTRL]
            controls = [ik_control, fk_control]
            for control in controls:
                cmds.addAttr(
                    control.ctrl,
                    proxy="%s.%s" % (self.limb_module_control.ctrl, IKFKSWITCH),
                    ln=IKFKSWITCH,
                    at="double",
                    min=0,
                    max=1,
                    dv=0,
                    keyable=True,
                )


class ModuleFinger:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.input = GuideList(guide)
        self.result_joint = JointChainSetup(guide, RESULT)
        self.fk = FKSetup(guide)
        self.ik = IKSetup(guide)
        self.limb_module_group = None
        self.limb_module_blend_map = {}

    def build(self):
        # Step 0: Create Module Group
        group_name = level_format(self.guide.module, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.limb_module_group = cmds.group(em=True, name=group_name)
            cmds.xform(self.limb_module_group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # Step 1: Build FK
        self.fk.build()

        # Step 2: Parent Items under Module Group
        cmds.parent(self.fk.fk_module_group, self.limb_module_group)


class ModuleHand:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.input = GuideList(guide)
        self.result_joint = JointChainSetup(guide, RESULT)
        self.fk = FKSetup(guide)
        self.ik = IKSetup(guide)
        self.limb_module_group = None
        self.limb_module_blend_map = {}

    def build(self):
        # Step 0: Create Module Group
        group_name = level_format(self.guide.module, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.limb_module_group = cmds.group(em=True, name=group_name)
            cmds.xform(self.limb_module_group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # Step 1: Build FK
        self.fk.build()

        # Step 2: Parent Items under Module Group
        cmds.parent(self.fk.fk_module_group, self.limb_module_group)


class ModuleSetup:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.input = GuideList(guide)
        self.builder_map = {LIMB: ModuleLimb, FINGER: ModuleFinger}

    def build(self):
        for g in self.input.guides:
            if g.module_start:
                builder_class = self.builder_map.get(g.module)
                if not builder_class:
                    print(f"{g.name} has no module, skipppz for now")
                    continue
                # print(g.name)
                builder_instance = builder_class(g.name)
                builder_instance.build()

    def assembly(self):
        pass
