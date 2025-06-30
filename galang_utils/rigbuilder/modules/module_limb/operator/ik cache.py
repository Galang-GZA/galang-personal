from maya import cmds
from typing import Dict
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_limb.rule.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.component.zcomponent import *


class LimbIKOperator:
    def __init__(self, component: LimbComponent):
        self.ik_map = component.ik.map
        self.handle = component.ik.handle
        self.guides = component.ik.module.guides
        self.side = component.ik.module.guide.side
        self.guides_end = component.ik.module.guides_end
        self.comp_static_map = component.ik.comp_static_map
        self.comp_active_map = component.ik.comp_active_map
        self.map: Dict = {}

    def _connect_distance(self, loc_start: str, loc_end: str, dist: str):
        cmds.connectAttr(f"{loc_start}.worldPosition[0]", f"{dist}.startPoint", force=True)
        cmds.connectAttr(f"{loc_end}.worldPosition[0]", f"{dist}.endPoint", force=True)

    def run(self):
        # Step 0 : Connect controls to joints
        for index, guide in enumerate(self.guides + self.guides_end):
            ik_control = self.ik_map[guide.name][CTRL].ctrl
            ik_joint = self.ik_map[guide.name][JNT]

            if index == 0:
                cmds.pointConstraint(ik_control, ik_joint)
                cmds.scaleConstraint(ik_control, ik_joint)
            if index == 1:
                cmds.poleVectorConstraint(ik_control, self.handle)
            if index == 2:
                cmds.orientConstraint(ik_control, ik_joint)
                cmds.scaleConstraint(ik_control, ik_joint)

        # Step 1 : Ik features soft, stretch, elbow pin, elbow slide
        # PM = plus minus average, MD = multiply divide, BLEND = blend, COND = condition
        MD_ik_LimbUp_Normalise_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[0].name_raw, f"{MULT_DIV}_{NORMAL}", "001"),
        )
        MD_ik_LimbLow_Normalise_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[1].name_raw, f"{MULT_DIV}_{NORMAL}", "001"),
        )

        # --- Create soft math nodes ---
        PM_ik_Limb_ChainLenOri_001 = cmds.createNode(
            "plusMinusAverage ",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{PLUS_MINUS}_{LEN_ORI}", "001"),
        )
        PM_ik_Limb_Soft_001 = cmds.createNode(
            "plusMinusAverage ",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{PLUS_MINUS}_{SOFT}", "001"),
        )
        PM_ik_Limb_Soft_002 = cmds.createNode(
            "plusMinusAverage ",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{PLUS_MINUS}_{SOFT}", "002"),
        )
        PM_ik_Limb_Soft_003 = cmds.createNode(
            "plusMinusAverage ",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{PLUS_MINUS}_{SOFT}", "003"),
        )
        PM_ik_Limb_Soft_004 = cmds.createNode(
            "plusMinusAverage ",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{PLUS_MINUS}_{SOFT}", "004"),
        )

        MD_ik_Limb_Soft_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{MULT_DIV}_{SOFT}", "001"),
        )
        MD_ik_Limb_Soft_002 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{MULT_DIV}_{SOFT}", "002"),
        )
        MD_ik_Limb_Soft_003 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{MULT_DIV}_{SOFT}", "003"),
        )
        MD_ik_Limb_Soft_004 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{MULT_DIV}_{SOFT}", "004"),
        )

        MD_ik_Limb_Soft_Scaler_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{MULT_DIV}_{SOFT}_{SCALER}", "001"),
        )

        MD_ik_LimbAttr_Scaler_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{MULT_DIV}_{ATTR}_{SCALER}", "001"),
        )

        COND_ik_Leg_Soft_001 = cmds.createNode(
            "condition",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{CONDITION}_{SOFT}", "001"),
        )

        # --- Create stretch math nodes ---
        PM_ik_LimbUp_Stretch_001 = cmds.createNode(
            "plusMinusAverage ",
            name=limb_node_format(PJ, IK, self.side, self.guides[0].name_raw, f"{PLUS_MINUS}_{STRETCH}", "001"),
        )
        PM_ik_LimbLow_Stretch_001 = cmds.createNode(
            "plusMinusAverage ",
            name=limb_node_format(PJ, IK, self.side, self.guides[1].name_raw, f"{PLUS_MINUS}_{STRETCH}", "001"),
        )

        MD_ik_LimbUp_Stretch_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[0].name_raw, f"{MULT_DIV}_{STRETCH}", "001"),
        )
        MD_ik_LimbUp_Stretch_002 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[0].name_raw, f"{MULT_DIV}_{STRETCH}", "002"),
        )
        MD_ik_LimbUp_Stretch_003 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[0].name_raw, f"{MULT_DIV}_{STRETCH}", "003"),
        )
        MD_ik_LimbLow_Strretch_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{MULT_DIV}_{STRETCH}", "001"),
        )
        MD_ik_LimbLow_Strretch_002 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{MULT_DIV}_{STRETCH}", "002"),
        )
        MD_ik_LimbLow_Strretch_003 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{MULT_DIV}_{STRETCH}", "003"),
        )

        MD_ik_Leg_Stretch_Scaler_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{MULT_DIV}_{STRETCH}_{SCALER}", "001"),
        )

        # --- Create pin math nodes ---
        MD_ik_LimbUp_Pin_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[0].name_raw, f"{MULT_DIV}_{PIN}", "001"),
        )
        MD_ik_LimbLow_Pin_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[1].name_raw, f"{MULT_DIV}_{PIN}", "001"),
        )

        MD_ik_LimbUp_Pin_Scaler_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[0].name_raw, f"{MULT_DIV}_{PIN}_{SCALER}", "001"),
        )
        MD_ik_LimbLow_Pin_Scaler_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[1].name_raw, f"{MULT_DIV}_{PIN}_{SCALER}", "001"),
        )

        BLEND_ik_LimbUp_Pin_Scaler_001 = cmds.createNode(
            "blend ",
            name=limb_node_format(PJ, IK, self.side, self.guides[0].name_raw, f"{BLEND}_{PIN}_{SCALER}", "001"),
        )
        BLEND_ik_LimbLow_Pin_Scaler_001 = cmds.createNode(
            "blend ",
            name=limb_node_format(PJ, IK, self.side, self.guides[1].name_raw, f"{BLEND}_{PIN}_{SCALER}", "001"),
        )

        # --- Create slide math nodes ---
        PM_ik_LimbUp_Slide_001 = cmds.createNode(
            "plusMinusAverage ",
            name=limb_node_format(PJ, IK, self.side, self.guides[0].name_raw, f"{PLUS_MINUS}_{SLIDE}", "001"),
        )

        PM_ik_LimbUp_Slide_002 = cmds.createNode(
            "plusMinusAverage ",
            name=limb_node_format(PJ, IK, self.side, self.guides[0].name_raw, f"{PLUS_MINUS}_{SLIDE}", "002"),
        )
        PM_ik_LimbLow_Slide_001 = cmds.createNode(
            "plusMinusAverage ",
            name=limb_node_format(PJ, IK, self.side, self.guides[1].name_raw, f"{PLUS_MINUS}_{SLIDE}", "001"),
        )
        PM_ik_LimbLow_Slide_002 = cmds.createNode(
            "plusMinusAverage ",
            name=limb_node_format(PJ, IK, self.side, self.guides[1].name_raw, f"{PLUS_MINUS}_{SLIDE}", "002"),
        )

        MD_ik_LimbUp_Slide_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[0].name_raw, f"{MULT_DIV}_{SLIDE}", "001"),
        )
        MD_ik_LimbLow_Slide_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[1].name_raw, f"{MULT_DIV}_{SLIDE}", "001"),
        )

        MD_ik_Limb_Slide_Scaler_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{MULT_DIV}_{SLIDE}_{SCALER}", "001"),
        )
        MD_ik_Limb_Slide_Limiter_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[2].name_raw, f"{MULT_DIV}_{SLIDE}_{LIMITER}", "001"),
        )
        MD_ik_LimbUp_Slide_Scaler_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[0].name_raw, f"{MULT_DIV}_{SLIDE}_{SCALER}", "001"),
        )
        MD_ik_LimbLow_Slide_Scaler_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[1].name_raw, f"{MULT_DIV}_{SLIDE}_{SCALER}", "001"),
        )

        COND_ik_LimbLow_Slide_001 = cmds.createNode(
            "multiplyDivide",
            name=limb_node_format(PJ, IK, self.side, self.guides[0].name_raw, f"{MULT_DIV}_{SLIDE}_{SCALER}", "001"),
        )

        # --- Define static and active components ---
        static0 = self.comp_static_map[self.guides[0].name]
        static1 = self.comp_static_map[self.guides[1].name]
        static2 = self.comp_static_map[self.guides[2].name]

        active0 = self.comp_active_map[self.guides[0].name]
        active1 = self.comp_active_map[self.guides[1].name]
        active2 = self.comp_active_map[self.guides[2].name]

        # --- Connect basic static and active components
        connection_pairs = [(0, 1), (1, 2), (0, 2)]
        for start_idx, end_idx in connection_pairs:
            g_start = self.guides[start_idx].name
            g_end = self.guides[end_idx].name

            for comp in [self.comp_static_map, self.comp_active_map]:
                loc_start = comp[g_start][LOCATOR]
                loc_end = comp[g_end][LOCATOR]
                dist = comp[g_start][DISTANCE]
                self._connect_distance(loc_start, loc_end, dist)

        # --- Connect soft, stretch components
        connections = [
            (active0[LOCATOR], active2[LOCATOR_BASE], active2[DISTANCE_BASE]),
            (active0[LOCATOR_SOFT], active2[LOCATOR_BLEND], active2[DISTANCE_BLEND]),
            (active0[LOCATOR], active2[LOCATOR_BLEND], active2[DISTANCE_STRETCH]),
        ]

        for loc_start, loc_end, dist in connections:
            self._connect_distance(loc_start, loc_end, dist)
