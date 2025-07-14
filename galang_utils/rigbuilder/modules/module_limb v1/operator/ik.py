from maya import cmds
from typing import Dict
from collections import defaultdict
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.constants import constant_project as const_proj
from galang_utils.rigbuilder.modules.module_limb.rule.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.component.zcomponent import *


class LimbIKOperator:
    def __init__(self, component: LimbComponent):
        self.module = component.ik.module
        self.ik_map = component.ik.map
        self.handle = component.ik.handle
        self.guides = component.ik.module.guides
        self.side = component.ik.module.guide.side
        self.guides_end = component.ik.module.guides_end
        self.comp_static_map = component.ik.comp_static_map
        self.comp_active_map = component.ik.comp_active_map

    def _connect_distance(self, loc_start: str, loc_end: str, dist: str):
        cmds.connectAttr(f"{loc_start}.worldPosition[0]", f"{dist}.startPoint", force=True)
        cmds.connectAttr(f"{loc_end}.worldPosition[0]", f"{dist}.endPoint", force=True)

    def run(self):
        guides = self.guides + self.guides_end
        up_control = self.ik_map[guides[0].name][const_proj.CTRL].ctrl
        mid_control = self.ik_map[guides[1].name][CTRL].ctrl
        ik_control = self.ik_map[guides[2].name][CTRL].ctrl
        axis_map = {"X": ".translateX", "Y": ".translateY", "Z": ".translateZ"}
        axis = axis_map.get(self.module.axis)
        LimbUp = guides[0].name_raw
        LimbLow = guides[1].name_raw
        LimbEnd = guides[2].name_raw

        # Step 0 : Connect controls to joints
        attrs = {
            SOFT: [0.0001, 100, 0.0001, "%s.%s" % (ik_control, SOFT)],
            STRETCH: [0.0, 1.0, 0.0, "%s.%s" % (ik_control, STRETCH)],
            PIN: [0.0, 1.0, 0.0, "%s.%s" % (ik_control, PIN)],
            SLIDE: [-1.0, 1.0, 0.0, "%s.%s" % (ik_control, SLIDE)],
        }
        for index, guide in enumerate(guides):
            control = self.ik_map[guide.name][CTRL].ctrl
            jnt = self.ik_map[guide.name][JNT]

            if index == 0:
                cmds.pointConstraint(control, jnt)
                cmds.scaleConstraint(control, jnt, mo=True)
            if index == 1:
                cmds.poleVectorConstraint(control, self.handle)
            if index == 2:
                cmds.orientConstraint(control, jnt)
                cmds.scaleConstraint(control, jnt, mo=True)
            if index in (0, 1):
                for attr, (min_val, max_val, default_val, proxy) in attrs.items():
                    if not cmds.attributeQuery(attr, node=control, exists=True):
                        cmds.addAttr(
                            control,
                            proxy=proxy,
                            ln=attr,
                            at="double",
                            min=min_val,
                            max=max_val,
                            dv=default_val,
                            keyable=True,
                        )

        # Step 1 : Set up math nodes for IK features
        # PM = plus minus average, MD = multiply divide, BLEND = blend, COND = condition
        if self.module.guide.side_id == MIRROR_SIDE_ID:
            node_normalization = [
                # Basic normalization
                ("multDoubleLinear", LimbUp, MD_Normal, "001", ".input2", -1.0),
                ("multDoubleLinear", LimbLow, MD_Normal, "001", ".input2", -1.0),
            ]
        else:
            node_normalization = [
                # Basic normalization
                ("multDoubleLinear", LimbUp, MD_Normal, "001", ".input2", 1.0),
                ("multDoubleLinear", LimbLow, MD_Normal, "001", ".input2", 1.0),
            ]

        node_defs = [
            # chain len
            ("plusMinusAverage", LimbEnd, PM_LenStatic, "001", ".operation", 1),
            ("plusMinusAverage", LimbEnd, PM_LenActive, "001", ".operation", 1),
            #
            # Soft math nodes
            ("plusMinusAverage", LimbEnd, PM_Soft, "001", ".operation", 2),
            ("plusMinusAverage", LimbEnd, PM_Soft, "002", ".operation", 2),
            ("plusMinusAverage", LimbEnd, PM_Soft, "003", ".operation", 2),
            ("plusMinusAverage", LimbEnd, PM_Soft, "004", ".operation", 2),
            ("multiplyDivide", LimbEnd, MD_Soft, "001", ".operation", 2),
            ("multDoubleLinear", LimbEnd, MD_Soft, "002", ".input2", -1.0),
            ("multiplyDivide", LimbEnd, MD_Soft, "003", ".operation", 3, ".input1X", 2.718),
            ("multDoubleLinear", LimbEnd, MD_Soft, "004"),
            ("multiplyDivide", LimbEnd, MD_Soft_Scaler, "001", ".operation", 2),
            ("multiplyDivide", LimbEnd, MD_Attr_Scaler, "001", ".operation", 2),
            ("condition", LimbEnd, COND_Soft, "001", ".operation", 2),
            #
            # Stretch
            ("plusMinusAverage", LimbUp, PM_Stretch, "001", ".operation", 1),
            ("plusMinusAverage", LimbLow, PM_Stretch, "001", ".operation", 1),
            ("multiplyDivide", LimbUp, MD_Stretch, "001", ".operation", 2),
            ("multDoubleLinear", LimbUp, MD_Stretch, "002"),
            ("multDoubleLinear", LimbUp, MD_Stretch, "003"),
            ("multiplyDivide", LimbLow, MD_Stretch, "001", ".operation", 2),
            ("multDoubleLinear", LimbLow, MD_Stretch, "002"),
            ("multDoubleLinear", LimbLow, MD_Stretch, "003"),
            ("multiplyDivide", LimbEnd, MD_Stretch_Scaler, "001", ".operation", 2),
            #
            # Pin
            ("multiplyDivide", LimbUp, MD_Pin_Scaler, "001", ".operation", 2),
            ("multiplyDivide", LimbLow, MD_Pin_Scaler, "001", ".operation", 2),
            ("blendTwoAttr", LimbUp, BLEND_Pin, "001"),
            ("blendTwoAttr", LimbLow, BLEND_Pin, "001"),
            #
            # Slide
            ("plusMinusAverage", LimbUp, PM_Slide, "001", ".operation", 2),
            ("plusMinusAverage", LimbUp, PM_Slide, "002", ".operation", 1),
            ("plusMinusAverage", LimbLow, PM_Slide, "001", ".operation", 2),
            ("plusMinusAverage", LimbLow, PM_Slide, "002", ".operation", 2),
            ("multiplyDivide", LimbEnd, MD_Slide_Scaler, "001", ".operation", 2),
            ("multiplyDivide", LimbEnd, MD_Slide_Limiter, "001"),
            ("multDoubleLinear", LimbUp, MD_Slide_Scaler, "001"),
            ("multDoubleLinear", LimbLow, MD_Slide_Scaler, "001"),
            ("condition", LimbEnd, COND_Slide, "001", ".operation", 2),
            #
            # Blend
            ("reverse", LimbEnd, REVERSE_STRETCH, "001"),
        ]
        nodes = defaultdict(lambda: defaultdict(dict))
        for node_type, guide_name, node_label, index, *rest in node_normalization + node_defs:
            attr1, p1, attr2, p2, attr3, p3 = (rest + [None, None, None, None, None, None])[:6]

            node_name = limb_node_format(PROJECT, IK, self.side, guide_name, node_label, index)
            node = cmds.createNode(node_type, n=node_name)
            nodes[guide_name][node_label][index] = node

            if attr1 is not None and p1 is not None:
                cmds.setAttr(f"{node}{attr1}", p1)
            if attr2 is not None and p2 is not None:
                cmds.setAttr(f"{node}{attr2}", p2)
            if attr3 is not None and p3 is not None:
                cmds.setAttr(f"{node}{attr3}", p3)

        # Step 2 : Connect locators to distance
        # Define static and active components
        static0 = self.comp_static_map[guides[0].name]
        static1 = self.comp_static_map[guides[1].name]
        static2 = self.comp_static_map[guides[2].name]

        active0 = self.comp_active_map[guides[0].name]
        active1 = self.comp_active_map[guides[1].name]
        active2 = self.comp_active_map[guides[2].name]

        # Connect basic static components
        connection_pairs = [(0, 1), (1, 2), (2, 0)]
        for start_idx, end_idx in connection_pairs:
            g_start = guides[start_idx].name
            g_end = guides[end_idx].name

            loc_start = self.comp_static_map[g_start][LOCATOR]
            loc_end = self.comp_static_map[g_end][LOCATOR]
            dist = self.comp_static_map[g_start][DISTANCE]
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
        cmds.pointConstraint(self.ik_map[guides[0].name][JNT], active0[LOCATOR])
        aimConstraint = cmds.aimConstraint(
            ik_control, active0[LOCATOR], aim=[1, 0, 0], wut="scene", u=(0.0, 1.0, 0.0), skip=["x", "z"]
        )
        cmds.delete(aimConstraint)
        aimConstraint = cmds.aimConstraint(
            ik_control, active0[LOCATOR], aim=[1, 0, 0], wut="scene", u=(0.0, 1.0, 0.0), mo=True
        )

        # Connect blend locator to ik control and active end locator
        BlendConstraint = cmds.pointConstraint(
            [self.ik_map[guides[2].name].get(CTRL).ctrl, active2[LOCATOR]], active2[LOCATOR_BLEND]
        )[0]

        # Connect ik control to active pole vector locator and stretch locator
        cmds.pointConstraint(self.ik_map[guides[1].name].get(CTRL).ctrl, active1[LOCATOR])
        cmds.pointConstraint(self.ik_map[guides[2].name].get(CTRL).ctrl, active2[LOCATOR_STRETCH])

        # Connect blend locator to ik handle
        cmds.pointConstraint(active2[LOCATOR_BLEND], self.handle)

        # Connect ik control to end active locator group
        cmds.pointConstraint(ik_control, active2[LOCATOR_GROUP])

        # Parent end active locators to root active locator
        cmds.parent(active2[LOCATOR_BASE], active0[LOCATOR])
        cmds.parent(active2[LOCATOR_GROUP], active0[LOCATOR])

        # Step 4 : Connect the nodes
        if self.module.guide.side_id == MIRROR_SIDE_ID:
            mirror_connection = [
                # limb soft average 4
                (f'{nodes[LimbEnd][COND_Soft]["001"]}.outColorR', f'{nodes[LimbEnd][PM_Soft]["004"]}.input1D[1]'),
                (f'{nodes[LimbEnd][MD_Soft_Scaler]["001"]}.outputX', f'{nodes[LimbEnd][PM_Soft]["004"]}.input1D[0]'),
            ]
        else:
            mirror_connection = [
                # limb soft average 4
                (f'{nodes[LimbEnd][COND_Soft]["001"]}.outColorR', f'{nodes[LimbEnd][PM_Soft]["004"]}.input1D[0]'),
                (f'{nodes[LimbEnd][MD_Soft_Scaler]["001"]}.outputX', f'{nodes[LimbEnd][PM_Soft]["004"]}.input1D[1]'),
            ]

        connections = [
            # static limb chain len 1
            (f"{static0[DISTANCE]}.distance", f'{nodes[LimbEnd][PM_LenStatic]["001"]}.input1D[0]'),
            (f"{static1[DISTANCE]}.distance", f'{nodes[LimbEnd][PM_LenStatic]["001"]}.input1D[1]'),
            #
            #
            #
            # Soft connections
            # limb attribute scaler 1
            (f"{active2[DISTANCE_BASE]}.distance", f'{nodes[LimbEnd][MD_Attr_Scaler]["001"]}.input1X'),
            (f"{static2[DISTANCE]}.distance", f'{nodes[LimbEnd][MD_Attr_Scaler]["001"]}.input2X'),
            #
            # limb soft average 1
            (f'{nodes[LimbEnd][PM_LenStatic]["001"]}.output1D', f'{nodes[LimbEnd][PM_Soft]["001"]}.input1D[0]'),
            (f"{ik_control}.{SOFT}", f'{nodes[LimbEnd][PM_Soft]["001"]}.input1D[1]'),
            #
            # limb soft scaler 1
            (f"{active2[DISTANCE]}.distance", f'{nodes[LimbEnd][MD_Soft_Scaler]["001"]}.input1X'),
            (f'{nodes[LimbEnd][MD_Attr_Scaler]["001"]}.outputX', f'{nodes[LimbEnd][MD_Soft_Scaler]["001"]}.input2X'),
            #
            # limb soft average 2
            (f'{nodes[LimbEnd][PM_Soft]["001"]}.output1D', f'{nodes[LimbEnd][PM_Soft]["002"]}.input1D[1]'),
            (f'{nodes[LimbEnd][MD_Soft_Scaler]["001"]}.outputX', f'{nodes[LimbEnd][PM_Soft]["002"]}.input1D[0]'),
            #
            # limb soft multiply divide 1
            (f"{ik_control}.{SOFT}", f'{nodes[LimbEnd][MD_Soft]["001"]}.input2X'),
            (f'{nodes[LimbEnd][PM_Soft]["002"]}.output1D', f'{nodes[LimbEnd][MD_Soft]["001"]}.input1X'),
            #
            # limb soft multiply divide 2
            (f'{nodes[LimbEnd][MD_Soft]["001"]}.outputX', f'{nodes[LimbEnd][MD_Soft]["002"]}.input1'),
            #
            # limb soft multiply divide 3
            (f'{nodes[LimbEnd][MD_Soft]["002"]}.output', f'{nodes[LimbEnd][MD_Soft]["003"]}.input2X'),
            #
            # limb soft multiply divide 4
            (f'{nodes[LimbEnd][MD_Soft]["003"]}.outputX', f'{nodes[LimbEnd][MD_Soft]["004"]}.input1'),
            (f"{ik_control}.{SOFT}", f'{nodes[LimbEnd][MD_Soft]["004"]}.input2'),
            #
            # limb soft average 3
            (f'{nodes[LimbEnd][MD_Soft]["004"]}.output', f'{nodes[LimbEnd][PM_Soft]["003"]}.input1D[1]'),
            (f'{nodes[LimbEnd][PM_LenStatic]["001"]}.output1D', f'{nodes[LimbEnd][PM_Soft]["003"]}.input1D[0]'),
            #
            # limb soft condition 1
            (f'{nodes[LimbEnd][MD_Soft_Scaler]["001"]}.outputX', f'{nodes[LimbEnd][COND_Soft]["001"]}.colorIfFalseR'),
            (f'{nodes[LimbEnd][PM_Soft]["003"]}.output1D', f'{nodes[LimbEnd][COND_Soft]["001"]}.colorIfTrueR'),
            (f'{nodes[LimbEnd][MD_Soft_Scaler]["001"]}.outputX', f'{nodes[LimbEnd][COND_Soft]["001"]}.firstTerm'),
            (f'{nodes[LimbEnd][PM_Soft]["001"]}.output1D', f'{nodes[LimbEnd][COND_Soft]["001"]}.secondTerm'),
            #
            # # limb ik active locator
            (f'{nodes[LimbEnd][PM_Soft]["004"]}.output1D', f"{active2[LOCATOR]}{axis}"),
            #
            #
            #
            # Stretch connections
            # limb stretch scaler 1
            (f"{active2[DISTANCE_BLEND]}.distance", f'{nodes[LimbEnd][MD_Stretch_Scaler]["001"]}.input1X'),
            (
                f'{nodes[LimbEnd][MD_Attr_Scaler]["001"]}.outputX',
                f'{nodes[LimbEnd][MD_Stretch_Scaler]["001"]}.input2X',
            ),
            #
            # limb up stretch multiply divide 1
            (f"{static0[DISTANCE]}.distance", f'{nodes[LimbUp][MD_Stretch]["001"]}.input1X'),
            (f'{nodes[LimbEnd][PM_LenStatic]["001"]}.output1D', f'{nodes[LimbUp][MD_Stretch]["001"]}.input2X'),
            #
            # limb low stretch multiply divide 1
            (f"{static1[DISTANCE]}.distance", f'{nodes[LimbLow][MD_Stretch]["001"]}.input1X'),
            (f'{nodes[LimbEnd][PM_LenStatic]["001"]}.output1D', f'{nodes[LimbLow][MD_Stretch]["001"]}.input2X'),
            #
            # limb up stretch multiply divide 2
            (f'{nodes[LimbEnd][MD_Stretch_Scaler]["001"]}.outputX', f'{nodes[LimbUp][MD_Stretch]["002"]}.input1'),
            (f'{nodes[LimbUp][MD_Stretch]["001"]}.outputX', f'{nodes[LimbUp][MD_Stretch]["002"]}.input2'),
            #
            # limb low stretch multiply divide 2
            (f'{nodes[LimbEnd][MD_Stretch_Scaler]["001"]}.outputX', f'{nodes[LimbLow][MD_Stretch]["002"]}.input1'),
            (f'{nodes[LimbLow][MD_Stretch]["001"]}.outputX', f'{nodes[LimbLow][MD_Stretch]["002"]}.input2'),
            #
            # limb up stretch multiply divide 3
            (f'{nodes[LimbUp][MD_Stretch]["002"]}.output', f'{nodes[LimbUp][MD_Stretch]["003"]}.input1'),
            (f"{ik_control}.{STRETCH}", f'{nodes[LimbUp][MD_Stretch]["003"]}.input2'),
            #
            # limb low stretch multiply divide 3
            (f'{nodes[LimbLow][MD_Stretch]["002"]}.output', f'{nodes[LimbLow][MD_Stretch]["003"]}.input1'),
            (f"{ik_control}.{STRETCH}", f'{nodes[LimbLow][MD_Stretch]["003"]}.input2'),
            #
            # limb up stretch average 1
            (f"{static0[DISTANCE]}.distance", f'{nodes[LimbUp][PM_Stretch]["001"]}.input1D[1]'),
            (f'{nodes[LimbLow][MD_Stretch]["003"]}.output', f'{nodes[LimbUp][PM_Stretch]["001"]}.input1D[0]'),
            #
            # limb low stretch average 1
            (f"{static1[DISTANCE]}.distance", f'{nodes[LimbLow][PM_Stretch]["001"]}.input1D[1]'),
            (f'{nodes[LimbLow][MD_Stretch]["003"]}.output', f'{nodes[LimbLow][PM_Stretch]["001"]}.input1D[0]'),
            #
            #
            #
            # Hinge pin connections
            # limb up hinge pin multiply divide 1
            (f"{active0[DISTANCE]}.distance", f'{nodes[LimbUp][MD_Pin_Scaler]["001"]}.input1X'),
            (f'{nodes[LimbEnd][MD_Attr_Scaler]["001"]}.outputX', f'{nodes[LimbUp][MD_Pin_Scaler]["001"]}.input2X'),
            #
            # limb low hinge pin multiply divide 1
            (f"{active1[DISTANCE]}.distance", f'{nodes[LimbLow][MD_Pin_Scaler]["001"]}.input1X'),
            (f'{nodes[LimbEnd][MD_Attr_Scaler]["001"]}.outputX', f'{nodes[LimbLow][MD_Pin_Scaler]["001"]}.input2X'),
            #
            # limb up hinge pin blend 1
            (f"{ik_control}.{PIN}", f'{nodes[LimbUp][BLEND_Pin]["001"]}.attributesBlender'),
            (f'{nodes[LimbUp][PM_Slide]["002"]}.output1D', f'{nodes[LimbUp][BLEND_Pin]["001"]}.input[0]'),
            (f'{nodes[LimbUp][MD_Pin_Scaler]["001"]}.outputX', f'{nodes[LimbUp][BLEND_Pin]["001"]}.input[1]'),
            #
            # limb low hinge pin blend 1
            (f"{ik_control}.{PIN}", f'{nodes[LimbLow][BLEND_Pin]["001"]}.attributesBlender'),
            (f'{nodes[LimbLow][PM_Slide]["002"]}.output1D', f'{nodes[LimbLow][BLEND_Pin]["001"]}.input[0]'),
            (f'{nodes[LimbLow][MD_Pin_Scaler]["001"]}.outputX', f'{nodes[LimbLow][BLEND_Pin]["001"]}.input[1]'),
            #
            #
            #
            # Hinge slide connections
            # limb hinge slide scaler 1
            (f"{active2[DISTANCE_STRETCH]}.distance", f'{nodes[LimbEnd][MD_Slide_Scaler]["001"]}.input1X'),
            (f'{nodes[LimbEnd][MD_Attr_Scaler]["001"]}.outputX', f'{nodes[LimbEnd][MD_Slide_Scaler]["001"]}.input2X'),
            #
            # limb hinge slide limiter 1
            (f"{ik_control}.{SLIDE}", f'{nodes[LimbEnd][MD_Slide_Limiter]["001"]}.input1X'),
            #
            # limb up hinge slide average 1
            (f'{nodes[LimbEnd][MD_Slide_Scaler]["001"]}.outputX', f'{nodes[LimbUp][PM_Slide]["001"]}.input1D[0]'),
            (f'{nodes[LimbUp][PM_Stretch]["001"]}.output1D', f'{nodes[LimbUp][PM_Slide]["001"]}.input1D[1]'),
            #
            # limb low hinge slide average 1
            (f'{nodes[LimbEnd][MD_Slide_Scaler]["001"]}.outputX', f'{nodes[LimbLow][PM_Slide]["001"]}.input1D[0]'),
            (f'{nodes[LimbLow][PM_Stretch]["001"]}.output1D', f'{nodes[LimbLow][PM_Slide]["001"]}.input1D[1]'),
            #
            # limb up hinge slide average 2
            (f'{nodes[LimbUp][PM_Stretch]["001"]}.output1D', f'{nodes[LimbUp][PM_Slide]["002"]}.input1D[0]'),
            (f'{nodes[LimbEnd][COND_Slide]["001"]}.outColorR', f'{nodes[LimbUp][PM_Slide]["002"]}.input1D[1]'),
            #
            # limb low hinge slide average 2
            (f'{nodes[LimbLow][PM_Stretch]["001"]}.output1D', f'{nodes[LimbLow][PM_Slide]["002"]}.input1D[0]'),
            (f'{nodes[LimbEnd][COND_Slide]["001"]}.outColorR', f'{nodes[LimbLow][PM_Slide]["002"]}.input1D[1]'),
            #
            # limb up hinge slide multiply divide 1
            (f'{nodes[LimbUp][PM_Slide]["001"]}.output1D', f'{nodes[LimbUp][MD_Slide_Scaler]["001"]}.input1'),
            (f'{nodes[LimbEnd][MD_Slide_Limiter]["001"]}.outputX', f'{nodes[LimbUp][MD_Slide_Scaler]["001"]}.input2'),
            #
            # limb low hinge slide multiply divide 1
            (f'{nodes[LimbLow][PM_Slide]["001"]}.output1D', f'{nodes[LimbLow][MD_Slide_Scaler]["001"]}.input1'),
            (f'{nodes[LimbEnd][MD_Slide_Limiter]["001"]}.outputX', f'{nodes[LimbLow][MD_Slide_Scaler]["001"]}.input2'),
            #
            # limb hinge slide condition 1
            (f'{nodes[LimbLow][MD_Slide_Scaler]["001"]}.output', f'{nodes[LimbEnd][COND_Slide]["001"]}.colorIfFalseR'),
            (f'{nodes[LimbUp][MD_Slide_Scaler]["001"]}.output', f'{nodes[LimbEnd][COND_Slide]["001"]}.colorIfTrueR'),
            (f'{nodes[LimbEnd][MD_Slide_Limiter]["001"]}.outputX', f'{nodes[LimbEnd][COND_Slide]["001"]}.firstTerm'),
            #
            #
            #
            # Feature normalization
            (f'{nodes[LimbUp][BLEND_Pin]["001"]}.output', f'{nodes[LimbUp][MD_Normal]["001"]}.input1'),
            (f'{nodes[LimbLow][BLEND_Pin]["001"]}.output', f'{nodes[LimbLow][MD_Normal]["001"]}.input1'),
            #
            #
            #
            # Limb joint connection
            (f'{nodes[LimbUp][MD_Normal]["001"]}.output', f"{self.ik_map[guides[1].name].get(JNT)}{axis}"),
            (f'{nodes[LimbLow][MD_Normal]["001"]}.output', f"{self.ik_map[guides[2].name].get(JNT)}{axis}"),
            #
            #
            #
            # Blend Constraint
            (f"{ik_control}.{STRETCH}", f'{nodes[LimbEnd][REVERSE_STRETCH]["001"]}.inputX'),
            (f"{ik_control}.{STRETCH}", f"{BlendConstraint}.{self.ik_map[guides[2].name].get(CTRL).ctrl}W0"),
            (f'{nodes[LimbEnd][REVERSE_STRETCH]["001"]}.outputX', f"{BlendConstraint}.{active2[LOCATOR]}W1"),
        ]
        for input, output in connections + mirror_connection:
            cmds.connectAttr(input, output)
