from maya import cmds
from typing import Dict
from collections import defaultdict
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

        # Step 1 : Set up math nodes for IK features
        # PM = plus minus average, MD = multiply divide, BLEND = blend, COND = condition
        LimbUp = self.guides[0].name_raw
        LimbLow = self.guides[1].name_raw
        LimbEnd = self.guides[2].name_raw

        node_defs = [
            # Basic normalisation
            ("multiplyDivide", LimbUp, MD_Normal, "001", ".input2", -1),
            ("multiplyDivide", LimbLow, MD_Normal, "001", ".input2", -1),
            ("plusMinusAverage", LimbEnd, PM_LenStatic, "001", ".operation", 1),
            ("plusMinusAverage", LimbEnd, PM_LenActive, "001", ".operation", 1),
            # Soft math nodes
            ("plusMinusAverage", LimbEnd, PM_Soft, "001", ".operation", 2),
            ("plusMinusAverage", LimbEnd, PM_Soft, "002", ".operation", 2),
            ("plusMinusAverage", LimbEnd, PM_Soft, "003", ".operation", 2),
            ("plusMinusAverage", LimbEnd, PM_Soft, "004", ".operation", 2),
            ("multiplyDivide", LimbEnd, MD_Soft, "001", ".operation", 2),
            ("multiplyDivide", LimbEnd, MD_Soft, "002", ".input2", -1),
            ("multiplyDivide", LimbEnd, MD_Soft, "003", ".operation", 3, ".input1", 2.718),
            ("multDoubleLinear", LimbEnd, MD_Soft, "004"),
            ("multiplyDivide", LimbEnd, MD_Soft_Scaler, "001", ".operation", 2),
            ("multiplyDivide", LimbEnd, MD_Attr_Scaler, "001", ".operation", 2),
            ("condition", LimbEnd, COND_Soft, "001", ".operation", 2),
            # Stretch
            ("plusMinusAverage", LimbUp, PM_Stretch, "001", "001", ".operation", 1),
            ("plusMinusAverage", LimbLow, PM_Stretch, "001", "001", ".operation", 1),
            ("multiplyDivide", LimbUp, MD_Stretch, "001", ".operation", 2),
            ("multDoubleLinear", LimbUp, MD_Stretch, "002"),
            ("multDoubleLinear", LimbUp, MD_Stretch, "003"),
            ("multiplyDivide", LimbLow, MD_Stretch, "001", ".operation", 2),
            ("multDoubleLinear", LimbLow, MD_Stretch, "002"),
            ("multDoubleLinear", LimbLow, MD_Stretch, "003"),
            ("multiplyDivide", LimbEnd, MD_Stretch_Scaler, "001", ".operation", 2),
            # Pin
            ("multiplyDivide", LimbUp, MD_Pin, "001", ".operation", 2),
            ("multiplyDivide", LimbLow, MD_Pin, "001", ".operation", 2),
            ("blend", LimbUp, BLEND_Pin_Scaler, "001"),
            ("blend", LimbLow, BLEND_Pin_Scaler, "001"),
            # Slide
            ("plusMinusAverage", LimbUp, PM_Slide, "001", ".operation", 2),
            ("plusMinusAverage", LimbUp, PM_Slide, "002", ".operation", 1),
            ("plusMinusAverage", LimbLow, PM_Slide, "001", ".operation", 2),
            ("plusMinusAverage", LimbLow, PM_Slide, "002", ".operation", 1),
            ("multiplyDivide", LimbEnd, MD_Slide_Scaler, "001", ".operation", 2),
            ("multiplyDivide", LimbEnd, MD_Slide_Limiter, "001"),
            ("multDoubleLinear", LimbUp, MD_Slide_Scaler, "001"),
            ("multDoubleLinear", LimbLow, MD_Slide_Scaler, "001"),
            ("condition", LimbEnd, COND_Slide, "001", ".operation", 2),
        ]
        nodes = defaultdict(lambda: defaultdict(dict))
        for node_type, guide_name, node_label, index, *rest in node_defs:
            attr1, p1, attr2, p2 = (rest + [None, None, None, None])[:4]

            node_name = limb_node_format(PJ, IK, self.side, guide_name, node_label, index)
            node = cmds.createNode(node_type, n=node_name)
            nodes[guide_name][node_label][index] = node

            if attr1 is not None and p1 is not None:
                cmds.setAttr(f"{node}{attr1}", p1)
            if attr2 is not None and p2 is not None:
                cmds.setAttr(f"{node}{attr2}", p2)

        # Step 2 : Connect locators to distance
        # Define static and active components
        static0 = self.comp_static_map[self.guides[0].name]
        static1 = self.comp_static_map[self.guides[1].name]
        static2 = self.comp_static_map[self.guides[2].name]

        active0 = self.comp_active_map[self.guides[0].name]
        active1 = self.comp_active_map[self.guides[1].name]
        active2 = self.comp_active_map[self.guides[2].name]

        # Connect basic static and active components
        connection_pairs = [(0, 1), (1, 2), (0, 2)]
        for start_idx, end_idx in connection_pairs:
            g_start = self.guides[start_idx].name
            g_end = self.guides[end_idx].name

            for comp in [self.comp_static_map, self.comp_active_map]:
                loc_start = comp[g_start][LOCATOR]
                loc_end = comp[g_end][LOCATOR]
                dist = comp[g_start][DISTANCE]
                self._connect_distance(loc_start, loc_end, dist)

        # Connect soft, stretch components
        connections = [
            (active0[LOCATOR], active2[LOCATOR_BASE], active2[DISTANCE_BASE]),
            (active0[LOCATOR_SOFT], active2[LOCATOR_BLEND], active2[DISTANCE_BLEND]),
            (active0[LOCATOR], active2[LOCATOR_BLEND], active2[DISTANCE_STRETCH]),
        ]

        for loc_start, loc_end, dist in connections:
            self._connect_distance(loc_start, loc_end, dist)

        # Step 3 : Connect all nodes
        connections = [(f"{static0[DISTANCE]}.distance", f'{nodes[LimbEnd][PM_LenStatic]['001']}.input1D[0]'),
                       (f"{static1[DISTANCE]}.distance", f'{nodes[LimbEnd][PM_LenStatic]['001']}.input1D[1]'),
                       (f'{active2[DISTANCE_BASE]}.distance', f'{nodes[LimbEnd][MD_Attr_Scaler]['001']}.input1X'),
                       (f'{active2[DISTANCE_BASE]}.distance', f'{nodes[LimbEnd][MD_Attr_Scaler]['001']}.input1X'),
                       ]
