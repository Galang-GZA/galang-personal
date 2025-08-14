from maya import cmds
from galang_utils.rigbuilder.constant.constant_project import *
from galang_utils.rigbuilder.constant.project import role as role
from galang_utils.rigbuilder.constant.project import setup as setup

from galang_utils.rigbuilder.modules.limb.program.node import NodeCreator
from galang_utils.rigbuilder.modules.limb.component.zcomponent import LimbComponent


class LimbIKOperator:
    def __init__(self, component: LimbComponent):
        self.guides = component.ik.module.guides
        self.side = component.ik.module.side
        self.axis = component.ik.module.axis
        self.side_id = component.ik.module.side_id

        self.joints = component.ik.joints
        self.controls = component.ik.controls
        self.handle = component.ik.handle

        self.static_comps = component.ik.static_comps
        self.active_comps = component.ik.active_comps

    def _connect_distance(self, loc_start: str, loc_end: str, dist: str):
        cmds.connectAttr(f"{loc_start}.worldPosition[0]", f"{dist}.startPoint", force=True)
        cmds.connectAttr(f"{loc_end}.worldPosition[0]", f"{dist}.endPoint", force=True)

    def run(self):
        up_control = self.controls[0].ctrl
        pv_control = self.controls[1].ctrl
        ik_control = self.controls[2].ctrl

        limb1 = self.guides[0].name_raw
        limb2 = self.guides[1].name_raw
        limb3 = self.guides[2].name_raw

        translate_axis_map = {"X": ".translateX", "Y": ".translateY", "Z": ".translateZ"}
        axis = translate_axis_map.get(self.axis)

        # Step 0 : Connect controls to joints
        attrs = {
            role.SOFT: [0.0001, 100, 0.0001, "%s.%s" % (ik_control, role.SOFT)],
            role.STRETCH: [0.0, 1.0, 0.0, "%s.%s" % (ik_control, role.STRETCH)],
            role.PIN: [0.0, 1.0, 0.0, "%s.%s" % (ik_control, role.PIN)],
            role.SLIDE: [-1.0, 1.0, 0.0, "%s.%s" % (ik_control, role.SLIDE)],
        }
        for i in range(len(self.guides)):
            if i == 0:
                cmds.pointConstraint(self.controls[i].ctrl, self.joints[i])
                cmds.scaleConstraint(self.controls[i].ctrl, self.joints[i], mo=True)
            if i == 1:
                cmds.poleVectorConstraint(self.controls[i].ctrl, self.handle)
            if i == 2:
                cmds.orientConstraint(self.controls[i].ctrl, self.joints[i])
                cmds.scaleConstraint(self.controls[i].ctrl, self.joints[i], mo=True)
            if i in (0, 1):
                for attr, (min_val, max_val, default_val, proxy) in attrs.items():
                    if not cmds.attributeQuery(attr, node=self.controls[i], exists=True):
                        cmds.addAttr(
                            self.controls[i].ctrl,
                            proxy=proxy,
                            ln=attr,
                            at="double",
                            min=min_val,
                            max=max_val,
                            dv=default_val,
                            keyable=True,
                        )

        # Step 1 : Set up math nodes for IK features
        # Setup normalization nodes
        node = NodeCreator(self.side, role.IK)
        if self.side_id == setup.MIRROR_SIDE_ID:
            limb1_normalize_multDiv_1 = node.setup(limb1, role.MULT_DIV, role.NORMAL, i=1, attr1="input2X", val1=-1.0)
            limb2_normalize_multDiv_1 = node.setup(limb2, role.MULT_DIV, role.NORMAL, i=1, attr1="input2X", val1=-1.0)
        else:
            limb1_normalize_multDiv_1 = node.setup(limb1, role.MULT_DIV, role.NORMAL, i=1, attr1="input2X", val1=1.0)
            limb2_normalize_multDiv_1 = node.setup(limb2, role.MULT_DIV, role.NORMAL, i=1, attr1="input2X", val1=1.0)

        #
        # Setup chain len nodes
        limb3_LenStatic_plusMin_1 = node.setup(limb3, role.PLUS_MIN, role.STATIC, i=1, attr1="operation", val1=1)
        limb3_LenActive_plusMin_1 = node.setup(limb3, role.PLUS_MIN, role.ACTIVE, i=1, attr1="operation", val1=1)

        #
        # Setup soft math nodes
        limb3_soft_plusMin_1 = node.setup(limb3, role.PLUS_MIN, role.SOFT, i=1, attr1="operation", val1=2)
        limb3_soft_plusMin_2 = node.setup(limb3, role.PLUS_MIN, role.SOFT, i=2, attr1="operation", val1=2)
        limb3_soft_plusMin_3 = node.setup(limb3, role.PLUS_MIN, role.SOFT, i=3, attr1="operation", val1=2)
        limb3_soft_plusMin_4 = node.setup(limb3, role.PLUS_MIN, role.SOFT, i=4, attr1="operation", val1=2)

        limb3_soft_multDiv_1 = node.setup(limb3, role.MULT_DIV, role.SOFT, i=1, attr1="operation", val1=2)
        limb3_soft_multDiv_2 = node.setup(limb3, role.MULT_DIV, role.SOFT, i=2, attr1="input2X", val1=-1.0)
        limb3_soft_multDiv_3 = node.setup(
            limb3, role.MULT_DIV, role.SOFT, i=3, attr1="operation", val1=3, attr2=".input1X", val2=2.718
        )
        limb3_soft_multDiv_4 = node.setup(limb3, role.MULT_DIV, role.SOFT, i=4)

        limb3_softScaler_multDiv_1 = node.setup(
            limb3, role.MULT_DIV, role.SOFT, role.SCALER, i=1, attr1="operation", val1=2
        )
        limb3_attrScaler_multDiv_1 = node.setup(
            limb3, role.MULT_DIV, role.ATTR, role.SCALER, i=1, attr1="operation", val1=2
        )

        limb3_soft_cond_1 = node.setup(limb3, role.MULT_DIV, role.SOFT, i=1, attr1="operation", val1=2)

        # Setup stretch math nodes
        limb1_stretch_plusMin_1 = node.setup(limb1, role.PLUS_MIN, role.STRETCH, i=1, attr1="operation", val1=1)
        limb2_stretch_plusMin_1 = node.setup(limb2, role.PLUS_MIN, role.STRETCH, i=1, attr1="operation", val1=1)

        limb1_stretch_multDiv_1 = node.setup(limb1, role.MULT_DIV, role.STRETCH, i=1, attr1="operation", val1=2)
        limb1_stretch_multDiv_2 = node.setup(limb1, role.MULT_DIV, role.STRETCH, i=2)
        limb1_stretch_multDiv_3 = node.setup(limb1, role.MULT_DIV, role.STRETCH, i=3)
        limb2_stretch_multDiv_1 = node.setup(limb2, role.MULT_DIV, role.STRETCH, i=1, attr1="operation", val1=2)
        limb2_stretch_multDiv_2 = node.setup(limb2, role.MULT_DIV, role.STRETCH, i=2)
        limb2_stretch_multDiv_3 = node.setup(limb2, role.MULT_DIV, role.STRETCH, i=3)

        limb3_stretchScaler_multDiv_1 = node.setup(
            limb3, role.MULT_DIV, role.STRETCH, role.SCALER, i=1, attr1="operation", val1=2
        )

        # Setup pin math nodes
        limb1_pinScaler_multDiv_1 = node.setup(
            limb1, role.MULT_DIV, role.PIN, role.SCALER, i=1, attr1="operation", val1=2
        )
        limb2_pinScaler_multDiv_1 = node.setup(
            limb2, role.MULT_DIV, role.PIN, role.SCALER, i=1, attr1="operation", val1=2
        )

        limb1_pin_blend_1 = node.setup(limb1, role.BLEND, role.PIN, i=1)
        limb2_pin_blend_1 = node.setup(limb2, role.BLEND, role.PIN, i=1)

        # Setup slide math nodes
        limb1_slide_plusMin_1 = node.setup(limb1, role.PLUS_MIN, i=1, attr1="operation", val1=2)
        limb1_slide_plusMin_2 = node.setup(limb1, role.PLUS_MIN, i=2, attr1="operation", val1=2)
        limb2_slide_plusMin_1 = node.setup(limb2, role.PLUS_MIN, i=1, attr1="operation", val1=2)
        limb2_slide_plusMin_2 = node.setup(limb2, role.PLUS_MIN, i=2, attr1="operation", val1=2)

        limb3_slide_cond_1 = node.setup(limb3, role.CONDITION, i=1, attr="operation", val1=2)

        limb1_slideScaler_multDiv_1 = node.setup(limb1, role.MULT_DIV, role.SCALER, i=1)
        limb2_slideScaler_multDiv_1 = node.setup(limb2, role.MULT_DIV, role.SCALER, i=1)
        limb3_slideScaler_multDiv_1 = node.setup(limb3, role.MULT_DIV, i=1, attr1="operation", val1=2)
        limb3_slideLimiter_multDiv_1 = node.setup(limb3, role.MULT_DIV, i=1)

        # Setup blend math nodes
        limb3_stretch_reverse_1 = node.setup(limb3, role.REVERSE, role.STRETCH, i=1)

        # Step 2 : Connect locators to distance
        # Define static and active components
        static0 = self.static_comps[self.guides[0].name]
        static1 = self.static_comps[self.guides[1].name]
        static2 = self.static_comps[self.guides[2].name]

        active0 = self.active_comps[self.guides[0].name]
        active1 = self.active_comps[self.guides[1].name]
        active2 = self.active_comps[self.guides[2].name]

        # Connect basic static components
        connection_pairs = [(0, 1), (1, 2), (2, 0)]
        for start_idx, end_idx in connection_pairs:
            g_start = self.guides[start_idx].name
            g_end = self.guides[end_idx].name

            loc_start = self.static_comps[g_start][role.LOCATOR]
            loc_end = self.static_comps[g_end][role.LOCATOR]
            dist = self.static_comps[g_start][role.DISTANCE]
            self._connect_distance(loc_start, loc_end, dist)

        # Connect soft, stretch components
        connections = [
            (active0[LOCATOR], active1[LOCATOR], active0[DISTANCE]),
            (active1[LOCATOR], active2[LOCATOR_BLEND], active1[DISTANCE]),
            (active0[LOCATOR], active2[LOCATOR_STRETCH], active2[DISTANCE]),
            (active0[LOCATOR], active2[LOCATOR_BASE], active2[DISTANCE_BASE]),
            (active2[LOCATOR], active2[LOCATOR_BLEND], active2[DISTANCE_BLEND]),
            (active0[LOCATOR], active2[LOCATOR_BLEND], active2[DISTANCE_STRETCH]),
        ]

        for loc_start, loc_end, dist in connections:
            self._connect_distance(loc_start, loc_end, dist)

        # Step 3 : Constraint locators
        # Aim connect - delete - re-aim connect root active locator to ik control
        cmds.pointConstraint(self.joints[0], active0[LOCATOR])
        aimConstraint = cmds.aimConstraint(
            ik_control, active0[LOCATOR], aim=[1, 0, 0], wut="scene", u=(0.0, 1.0, 0.0), skip=["x", "z"]
        )
        cmds.delete(aimConstraint)
        aimConstraint = cmds.aimConstraint(
            ik_control, active0[LOCATOR], aim=[1, 0, 0], wut="scene", u=(0.0, 1.0, 0.0), mo=True
        )

        # Connect blend locator to ik control and active end locator
        BlendConstraint = cmds.pointConstraint([self.controls[2].ctrl, active2[LOCATOR]], active2[LOCATOR_BLEND])[0]

        # Connect ik control to active pole vector locator and stretch locator
        cmds.pointConstraint(self.controls[1].ctrl, active1[LOCATOR])
        cmds.pointConstraint(self.controls[2].ctrl, active2[LOCATOR_STRETCH])

        # Connect blend locator to ik handle
        cmds.pointConstraint(active2[LOCATOR_BLEND], self.handle)

        # Connect ik control to end active locator group
        cmds.pointConstraint(ik_control, active2[LOCATOR_GROUP])

        # Parent end active locators to root active locator
        cmds.parent(active2[LOCATOR_BASE], active0[LOCATOR])
        cmds.parent(active2[LOCATOR_GROUP], active0[LOCATOR])

        # Step 4 : Connect the nodes
        if self.side_id == MIRROR_SIDE_ID:
            cmds.connectAttr(f"{limb3_soft_cond_1}.outColorR", f"{limb3_soft_plusMin_4}.input1D[1]")
            cmds.connectAttr(f"{limb3_softScaler_multDiv_1}.outputX", f"{limb3_soft_plusMin_4}.input1D[0]")
        else:
            cmds.connectAttr(f"{limb3_soft_cond_1}.outColorR", f"{limb3_soft_plusMin_4}.input1D[0]")
            cmds.connectAttr(f"{limb3_softScaler_multDiv_1}", f"{limb3_soft_plusMin_4}.input1D[1]")

        # static limb chain len 1
        cmds.connectAttr(f"{static0[DISTANCE]}.distance", f"{limb3_LenStatic_plusMin_1}.input1D[0]")
        cmds.connectAttr(f"{static1[DISTANCE]}.distance", f"{limb3_LenStatic_plusMin_1}.input1D[0]")

        # limb attribute scaler 1
        cmds.connectAttr(f"{active2[DISTANCE_BASE]}.distance", f"{limb3_attrScaler_multDiv_1}.input1X")
        cmds.connectAttr(f"{static2[DISTANCE]}.distance", f"{limb3_attrScaler_multDiv_1}.input2X")

        # Soft connections
        # limb soft average 1
        cmds.connectAttr(f"{limb3_LenStatic_plusMin_1}.output1D", f"{limb3_soft_plusMin_1}.input1D[0]")
        cmds.connectAttr(f"{ik_control}.{role.SOFT}", f"{limb3_soft_plusMin_1}.input1D[1]")

        # limb soft scaler 1
        cmds.connectAttr(f"{active2[DISTANCE]}", f"{limb3_softScaler_multDiv_1}.input1X")
        cmds.connectAttr(f"{limb3_attrScaler_multDiv_1}.outputX", f"{limb3_softScaler_multDiv_1}.input2X")

        # limb soft average 2
        cmds.connectAttr(f"{limb3_soft_plusMin_1}.output1D", f"{limb3_soft_plusMin_2}.input1D[1]")
        cmds.connectAttr(f"{limb3_softScaler_multDiv_1}.outputX", f"{limb3_soft_plusMin_2}.input1D[0]")

        # limb soft multiply divide 1
        cmds.connectAttr(f"{ik_control}.{SOFT}", f"{limb3_soft_multDiv_1}.input2X")
        cmds.connectAttr(f"{limb3_soft_plusMin_2}.output1D", f"{limb3_soft_multDiv_1}.input1X")

        # limb soft multiply divide 2
        cmds.connectAttr(f"{limb3_soft_multDiv_1}.outputX", f"{limb3_soft_multDiv_2}.input1X")

        # limb soft multiply divide 3
        cmds.connectAttr(f"{limb3_soft_multDiv_2}.outputX", f"{limb3_soft_multDiv_3}.input2X")

        # limb soft multiply divide 4
        cmds.connectAttr(f"{limb3_soft_multDiv_3}.outputX", f"{limb3_soft_multDiv_4}.input1X")
        cmds.connectAttr(f"{ik_control}.{SOFT}", f"{limb3_soft_multDiv_4}.input2X")

        # limb soft average 3
        cmds.connectAttr(f"{limb3_soft_multDiv_4}.outputX", f"{limb3_soft_plusMin_3}.input1D[1]")
        cmds.connectAttr(f"{limb3_LenStatic_plusMin_1}.output1D", f"{limb3_soft_plusMin_3}.input1D[0]")

        # limb soft condition 1
        cmds.connectAttr(f"{limb3_softScaler_multDiv_1}.outputX", f"{limb3_soft_cond_1}.colorIfFalseR")
        cmds.connectAttr(f"{limb3_soft_plusMin_3}.output1D", f"{limb3_soft_cond_1}.colorIfTrueR")
        cmds.connectAttr(f"{limb3_softScaler_multDiv_1}.outputX", f"{limb3_soft_cond_1}.firstTerm")
        cmds.connectAttr(f"{limb3_soft_plusMin_1}.output1D", f"{limb3_soft_cond_1}.secondTerm")

        # limb ik active locator
        cmds.connectAttr(f"{limb3_soft_plusMin_4}.output1D", f"{active2[LOCATOR]}{axis}")

        # Stretch connections
        # limb stretch scaler 1
        cmds.connectAttr(f"{active2[DISTANCE_BLEND]}.distance", f"{limb3_stretchScaler_multDiv_1}.input1X")
        cmds.connectAttr(f"{limb3_attrScaler_multDiv_1}.outputX", f"{limb3_stretchScaler_multDiv_1}.input2X")

        # limb up stretch multiply divide 1
        cmds.connectAttr(f"{static0[DISTANCE]}.distance", f"{limb1_stretch_multDiv_1}.input1X")
        cmds.connectAttr(f"{limb3_LenStatic_plusMin_1}.output1D", f"{limb1_stretch_multDiv_1}.input2X")

        # limb low stretch multiply divide 1
        cmds.connectAttr(f"{static1[DISTANCE]}.distance", f"{limb2_stretch_multDiv_1}.input1X")
        cmds.connectAttr(f"{limb3_LenStatic_plusMin_1}.output1D", f"{limb2_stretch_multDiv_1}.input2X")

        # limb up stretch multiply divide 2
        cmds.connectAttr(f"{limb3_stretchScaler_multDiv_1}.outputX", f"{limb1_stretch_multDiv_2}.input1X")
        cmds.connectAttr(f"{limb1_stretch_multDiv_1}.outputX", f"{limb1_stretch_multDiv_2}.input2X")

        # limb low stretch multiply divide 2
        cmds.connectAttr(f"{limb3_stretchScaler_multDiv_1}.outputX", f"{limb2_stretch_multDiv_2}.input1X")
        cmds.connectAttr(f"{limb2_stretch_multDiv_1}.outputX", f"{limb2_stretch_multDiv_2}.input2X")

        # limb up stretch multiply divide 3
        cmds.connectAttr(f"{limb1_stretch_multDiv_2}.outputX", f"{limb1_stretch_multDiv_3}.input1X")
        cmds.connectAttr(f"{ik_control}.{STRETCH}", f"{limb1_stretch_multDiv_3}.input2X")

        # limb low stretch multiply divide 3
        cmds.connectAttr(f"{limb2_stretch_multDiv_2}.outputX", f"{limb2_stretch_multDiv_3}.input1X")
        cmds.connectAttr(f"{ik_control}.{STRETCH}", f"{limb2_stretch_multDiv_3}.input2X")

        # limb up stretch average 1
        cmds.connectAttr(f"{static0[DISTANCE]}.distance", f"{limb1_stretch_plusMin_1}.input1D[1]")
        cmds.connectAttr(f"{limb2_stretch_multDiv_3}.outputX", f"{limb1_stretch_plusMin_1}.input1D[0]")

        # limb low stretch average 1
        cmds.connectAttr(f"{static1[DISTANCE]}.distance", f"{limb2_stretch_plusMin_1}.input1D[1]")
        cmds.connectAttr(f"{limb2_stretch_multDiv_3}.outputX", f"{limb2_stretch_plusMin_1}.input1D[0]")

        # Hinge pin connections
        # limb up hinge pin multiply divide 1
        cmds.connectAttr(f"{active0[DISTANCE]}.distance", f"{limb1_pinScaler_multDiv_1}.input1X")
        cmds.connectAttr(f"{limb3_attrScaler_multDiv_1}.outputX", f"{limb1_pinScaler_multDiv_1}.input2X")

        # limb low hinge pin multiply divide 1
        cmds.connectAttr(f"{active1[DISTANCE]}.distance", f"{limb2_pinScaler_multDiv_1}.input1X")
        cmds.connectAttr(f"{limb3_attrScaler_multDiv_1}.outputX", f"{limb2_pinScaler_multDiv_1}.input2X")

        # limb up hinge pin blend 1
        cmds.connectAttr(f"{ik_control}.{PIN}", f"{limb1_pin_blend_1}.attributesBlender")
        cmds.connectAttr(f"{limb1_slide_plusMin_2}.output1D", f"{limb1_pin_blend_1}.input[0]")
        cmds.connectAttr(f"{limb1_pinScaler_multDiv_1}.outputX", f"{limb1_pin_blend_1}.input[1]")

        # limb up hinge pin blend 1
        cmds.connectAttr(f"{ik_control}.{PIN}", f"{limb2_pin_blend_1}.attributesBlender")
        cmds.connectAttr(f"{limb2_slide_plusMin_2}.output1D", f"{limb2_pin_blend_1}.input[0]")
        cmds.connectAttr(f"{limb2_pinScaler_multDiv_1}.outputX", f"{limb2_pin_blend_1}.input[1]")

        # Hinge slide connections
        # limb hinge slide scaler 1
        cmds.connectAttr(f"{active2[DISTANCE_STRETCH]}.distance", f"{limb3_slideScaler_multDiv_1}.input1X")
        cmds.connectAttr(f"{limb3_attrScaler_multDiv_1}.outputX", f"{limb3_slideScaler_multDiv_1}.input2X")

        # limb hinge slide limiter 1
        cmds.connectAttr(f"{ik_control}.{SLIDE}", f"{limb3_slideLimiter_multDiv_1}.input1X")

        # limb up hinge slide average 1
        cmds.connectAttr(f"{limb3_slideScaler_multDiv_1}.outputX", f"{limb1_slide_plusMin_1}.input1D[0]")
        cmds.connectAttr(f"{limb1_stretch_plusMin_1}.output1D", f"{limb1_slide_plusMin_1}.input1D[1]")

        # limb low hinge slide average 1
        cmds.connectAttr(f"{limb3_slideScaler_multDiv_1}.outputX", f"{limb2_slide_plusMin_1}.input1D[0]")
        cmds.connectAttr(f"{limb2_stretch_plusMin_1}.output1D", f"{limb2_slide_plusMin_1}.input1D[1]")

        # limb up hinge slide average 2
        cmds.connectAttr(f"{limb1_stretch_plusMin_1}.output1D", f"{limb1_slide_plusMin_2}.input1D[0]")
        cmds.connectAttr(f"{limb3_slide_cond_1}.outColorR", f"{limb1_slide_plusMin_2}.input1D[1]")

        # limb low hinge slide average 2
        cmds.connectAttr(f"{limb2_stretch_plusMin_1}.output1D", f"{limb2_slide_plusMin_2}.input1D[0]")
        cmds.connectAttr(f"{limb3_slide_cond_1}.outColorR", f"{limb2_slide_plusMin_2}.input1D[1]")

        # limb up hinge slide multiply divide 1
        cmds.connectAttr(f"{limb1_slide_plusMin_1}.output1D", f"{limb1_slideScaler_multDiv_1}.input1X")
        cmds.connectAttr(f"{limb3_slideLimiter_multDiv_1}.outputX", f"{limb1_slideScaler_multDiv_1}.input2X")

        # limb low hinge slide multiply divide 1
        cmds.connectAttr(f"{limb2_slide_plusMin_1}.output1D", f"{limb2_slideScaler_multDiv_1}.input1X")
        cmds.connectAttr(f"{limb3_slideLimiter_multDiv_1}.outputX", f"{limb2_slideScaler_multDiv_1}.input2X")

        # limb hinge slide condition 1
        cmds.connectAttr(f"{limb2_slideScaler_multDiv_1}.outputX", f"{limb3_slide_cond_1}.colorIfFalseR")
        cmds.connectAttr(f"{limb1_slideScaler_multDiv_1}.outputX", f"{limb3_slide_cond_1}.colorIfTrueR")
        cmds.connectAttr(f"{limb3_slideLimiter_multDiv_1}.outputX", f"{limb3_slide_cond_1}.firstTerm")

        # Feature normalization
        cmds.connectAttr(f"{limb1_pin_blend_1}.outputX", f"{limb1_normalize_multDiv_1}.input1")
        cmds.connectAttr(f"{limb2_pin_blend_1}.outputX", f"{limb2_normalize_multDiv_1}.input1")

        # Limb joint connection
        cmds.connectAttr(f"{limb1_normalize_multDiv_1}.outputX", f"{self.joints[1]}{axis}")
        cmds.connectAttr(f"{limb2_normalize_multDiv_1}.outputX", f"{self.joints[2]}{axis}")

        # Blend Constraint
        cmds.connectAttr(f"{ik_control}.{STRETCH}", f"{limb3_stretch_reverse_1}.input1X")
        cmds.connectAttr(f"{ik_control}.{STRETCH}", f"{BlendConstraint}.{self.controls[2].ctrl}WO")
        cmds.connectAttr(f"{limb3_stretch_reverse_1}.outputX", f"{BlendConstraint}.{active2[LOCATOR]}W1")
