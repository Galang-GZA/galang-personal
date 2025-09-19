from maya import cmds
from typing import List

from rig_x_frame.constants.project import role as role
from rig_x_frame.constants.project import setup as setup
from rig_x_frame.constants.general import role as gen_role
from rig_x_frame.mod_zero.limb.component.setup_ik import LimbIKComponent
from rig_x_frame.mod_zero.base.operator.dg import Node
from rig_x_frame.mod_zero.base.operator.distance import DistanceNode, DistanceSet
from rig_x_frame.mod_zero.limb.component.zcomponents import LimbComponents


class LimbIKOperator(LimbIKComponent):
    def __init__(self, component: LimbComponents):
        super().__init__(component.module)
        module = component.module
        guides = module.guides
        self.side_id = module.side_id
        control_guides = [guides[0], module.guides_pv, guides[-1]]

        # Step 2: Setup IK attributes
        # Add attributes for soft, stretch, pin, slide
        cmds.setAttr("ikRPsolver.tolerance", 1e-007)
        attrs = {
            role.SOFT: [0.0001, 100, 0.0001],
            role.STRETCH: [0.0, 1.0, 0.0],
            role.PIN: [0.0, 1.0, 0.0],
            role.SLIDE: [-1.0, 1.0, 0.0],
        }
        for attr, (min_val, max_val, default_val) in attrs.items():
            if not cmds.attributeQuery(attr, node=self.controls[2], exists=True):
                cmds.addAttr(self.controls[2], ln=attr, at="double", dv=default_val, k=True, min=min_val, max=max_val)

        self.ik_component = component.ik
        # Pre compute dg components
        self.static_distances = DistanceSet(guides, module, [role.IK, role.STATIC])
        self.active_distances = DistanceSet(control_guides, module, [role.IK, role.ACTIVE])
        self.base_distance = DistanceNode(control_guides[2], module, [role.IK, role.ACTIVE, role.BASE])
        self.blend_distance = DistanceNode(control_guides[2], module, [role.IK, role.ACTIVE, role.BLEND])
        self.stretch_distance = DistanceNode(control_guides[2], module, [role.IK, role.ACTIVE, role.STRETCH])

        """ SOFT DKK PISAH PER FUNCTION BIAR GA BERANTAKAN"""
        # Pre compute math dg components
        # Argument for node types
        reverse = [role.IK, gen_role.REVERSE]
        reverse_stretch = reverse + [role.STRETCH]

        blend = [role.IK, gen_role.BLEND]
        blend_pin = blend + [role.PIN]

        mult_div = [role.IK, gen_role.MULT_DIV]
        mult_div_pin = mult_div + [role.PIN]
        mult_div_attr = mult_div + [role.ATTR]
        mult_div_soft = mult_div + [role.SOFT]
        mult_div_slide = mult_div + [role.SLIDE]
        mult_div_normal = mult_div + [role.NORMAL]
        mult_div_stretch = mult_div + [role.STRETCH]
        mult_div_pin_scaler = mult_div_pin + [role.SCALER]
        mult_div_soft_scaler = mult_div_soft + [role.SCALER]
        mult_div_attr_scaler = mult_div_attr + [role.SCALER]
        mult_div_slide_scaler = mult_div_slide + [role.SCALER]
        mult_div_stretch_scaler = mult_div_stretch + [role.SCALER]
        mult_div_slide_limiter = mult_div_slide + [role.LIMITER]

        plus_min = [role.IK, gen_role.PLUS_MIN]
        plus_min_soft = plus_min + [role.SOFT]
        plus_min_slide = plus_min + [role.SLIDE]
        plus_min_stretch = plus_min + [role.STRETCH]
        plus_min_static = plus_min + [role.STATIC]
        plus_min_active = plus_min + [role.ACTIVE]

        condition = [role.IK, gen_role.CONDITION]
        condition_soft = condition + [role.SOFT]
        condition_slide = condition + [role.SLIDE]

        # Normalization math nodes
        normal_input1 = {"input2X": -1.0 if self.side_id == setup.MIRROR_SIDE_ID else 1.0}
        normal_input2 = {"input2X": -1.0 if self.side_id == setup.MIRROR_SIDE_ID else 1.0}
        self.normalize1_multDiv = Node(guides[0], module, mult_div_normal, normal_input1)
        self.normalize2_multDiv = Node(guides[1], module, mult_div_normal, normal_input2)

        # Chain Len math nodes
        self.lenStatic_plusMin = Node(guides[2], module, plus_min_static, {"operation": 1})
        self.lenActive_plusMin = Node(guides[2], module, plus_min_active, {"operation": 1})

        # Setup soft math nodes
        self.soft_cond = Node(guides[2], module, condition_soft, {"operation": 2})
        self.soft_plusMin_1 = Node(guides[2], module, plus_min_soft + [1], {"operation": 2})
        self.soft_plusMin_2 = Node(guides[2], module, plus_min_soft + [2], {"operation": 2})
        self.soft_plusMin_3 = Node(guides[2], module, plus_min_soft + [3], {"operation": 2})
        self.soft_plusMin_4 = Node(guides[2], module, plus_min_soft + [4], {"operation": 2})
        self.soft_multDiv_1 = Node(guides[2], module, mult_div_soft + [1], {"operation": 2})
        self.soft_multDiv_2 = Node(guides[2], module, mult_div_soft + [2], {"input2X": -1.0})
        self.soft_multDiv_3 = Node(guides[2], module, mult_div_soft + [3], {"operation": 3, "input1X": 2.718})
        self.soft_multDiv_4 = Node(guides[2], module, mult_div_soft + [4])
        self.softScaler_multDiv = Node(guides[2], module, mult_div_soft_scaler, {"operation": 2})
        self.attrScaler_multDiv = Node(guides[2], module, mult_div_attr_scaler, {"operation": 2})

        # Setup stretch math nodes
        self.stretch1_plusMin_1 = Node(guides[0], module, plus_min_stretch + [1], {"operation": 1})
        self.stretch2_plusMin_1 = Node(guides[1], module, plus_min_stretch + [1], {"operation": 1})
        self.stretch1_multDiv_1 = Node(guides[0], module, mult_div_stretch + [1], {"operation": 2})
        self.stretch1_multDiv_2 = Node(guides[0], module, mult_div_stretch + [2])
        self.stretch1_multDiv_3 = Node(guides[0], module, mult_div_stretch + [3])
        self.stretch2_multDiv_1 = Node(guides[1], module, mult_div_stretch + [1], {"operation": 2})
        self.stretch2_multDiv_2 = Node(guides[1], module, mult_div_stretch + [2])
        self.stretch2_multDiv_3 = Node(guides[1], module, mult_div_stretch + [3])
        self.stretchScaler_multDiv = Node(guides[2], module, mult_div_stretch_scaler, {"operation": 2})

        # Setup pin math nodes
        self.pin1_blend = Node(guides[0], module, blend_pin, {"operation": 2})
        self.pin2_blend = Node(guides[1], module, blend_pin, {"operation": 2})
        self.pinScaler1_multDiv = Node(guides[0], module, mult_div_pin_scaler)
        self.pinScaler2_multDiv = Node(guides[1], module, mult_div_pin_scaler)

        # Setup slide math nodes
        self.slide_cond = Node(guides[2], module, condition_slide, {"operation": 2})
        self.slide1_plusMin_1 = Node(guides[0], module, plus_min_slide + [1], {"operation": 2})
        self.slide1_plusMin_2 = Node(guides[0], module, plus_min_slide + [2], {"operation": 2})
        self.slide2_plusMin_1 = Node(guides[1], module, plus_min_slide + [1], {"operation": 2})
        self.slide2_plusMin_2 = Node(guides[1], module, plus_min_slide + [2], {"operation": 2})
        self.slideScaler1_multDiv = Node(guides[0], module, mult_div_slide_scaler)
        self.slideScaler2_multDiv = Node(guides[1], module, mult_div_slide_scaler)
        self.slideScaler3_multDiv = Node(guides[2], module, mult_div_slide_scaler, {"operation": 2})
        self.slideLimiter_multDiv = Node(guides[2], module, mult_div_slide_limiter)

        # Setup blend math nodes
        self.stretch_reverse = Node(guides[3], module, reverse_stretch)

    def _connect_distance(self, loc_start: str, loc_end: str, dist: str):
        cmds.connectAttr(f"{loc_start}.worldPosition[0]", f"{dist}.startPoint", force=True)
        cmds.connectAttr(f"{loc_end}.worldPosition[0]", f"{dist}.endPoint", force=True)

    def run(self):
        statice_locators = self.ik_component.static_locators
        actve_locators = self.ik_component.active_locators
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # STEP 0 : CREATE PRE COMPUTED DG NODES
        # Create distance nodes
        components: List[Node] = [
            # distances
            self.static_distances,
            self.active_distances,
            self.base_distance,
            self.blend_distance,
            self.stretch_distance,
            # normalization
            self.normalize1_multDiv,
            self.normalize2_multDiv,
            # chain length
            self.lenStatic_plusMin,
            self.lenActive_plusMin,
            # soft math
            self.soft_cond,
            self.soft_plusMin_1,
            self.soft_plusMin_2,
            self.soft_plusMin_3,
            self.soft_plusMin_4,
            self.soft_multDiv_1,
            self.soft_multDiv_2,
            self.soft_multDiv_3,
            self.soft_multDiv_4,
            self.softScaler_multDiv,
            self.attrScaler_multDiv,
            # stretch math
            self.stretch1_plusMin_1,
            self.stretch2_plusMin_1,
            self.stretch1_multDiv_1,
            self.stretch1_multDiv_2,
            self.stretch1_multDiv_3,
            self.stretch2_multDiv_1,
            self.stretch2_multDiv_2,
            self.stretch2_multDiv_3,
            self.stretchScaler_multDiv,
            # pin math
            self.pin1_blend,
            self.pin2_blend,
            self.pinScaler1_multDiv,
            self.pinScaler2_multDiv,
            # slide math
            self.slide_cond,
            self.slide1_plusMin_1,
            self.slide1_plusMin_2,
            self.slide2_plusMin_1,
            self.slide2_plusMin_2,
            self.slideScaler1_multDiv,
            self.slideScaler2_multDiv,
            self.slideScaler3_multDiv,
            self.slideLimiter_multDiv,
            # blend math
            self.stretch_reverse,
        ]
        for component in components:
            component.create()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # STEP 1 : CONNECT CONTROLS TO JOINTS
        # Root control connection
        cmds.pointConstraint(self.controls[0], self.joints[0])
        cmds.scaleConstraint(self.controls[0], self.joints[0], mo=True)

        # Pole vector control connection
        cmds.poleVectorConstraint(self.controls[1], self.handle)

        # Handle control connection
        cmds.orientConstraint(self.controls[2], self.joints[2])
        cmds.scaleConstraint(self.controls[2], self.joints[2], mo=True)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # STEP 2 : PROXY ATTRIBUTES FROM HANDLE CONTROL TO OTHERS
        # Ik control attribute list with values and proxies
        attrs = {
            role.SOFT: [0.0001, 100, 0.0001, "%s.%s" % (self.controls[2], role.SOFT)],
            role.STRETCH: [0.0, 1.0, 0.0, "%s.%s" % (self.controls[2], role.STRETCH)],
            role.PIN: [0.0, 1.0, 0.0, "%s.%s" % (self.controls[2], role.PIN)],
            role.SLIDE: [-1.0, 1.0, 0.0, "%s.%s" % (self.controls[2], role.SLIDE)],
        }

        # Proxy Ik control attributes to root control
        for attr, (min_val, max_val, val, proxy) in attrs.items():
            cmds.addAttr(self.controls[0], proxy=proxy, ln=attr, at="double", min=min_val, max=max_val, dv=val)

        # Proxy Ik control attributes to pole vector control
        pv_attrs = {k: v for k, v in attrs.items() if k in (role.PIN, role.SLIDE)}
        for attr, (min_val, max_val, val, proxy) in pv_attrs.items():
            cmds.addAttr(self.controls[1], proxy=proxy, ln=attr, at="double", min=min_val, max=max_val, dv=val)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # STEP 3 : CONNECT LOCATORS TO DISTANCES
        connections = [
            (self.static_locators[0], self.static_locators[1], self.static_distances[0]),
            (self.static_locators[1], self.static_locators[2], self.static_distances[1]),
            (self.static_locators[2], self.static_locators[0], self.static_distances[2]),
            (self.active_locators[0], self.active_locators[1], self.active_distances[0]),
            (self.active_locators[1], self.blend_locator, self.active_distances[1]),
            (self.active_locators[0], self.stretch_locator, self.active_distances[2]),
            (self.active_locators[0], self.base_locator, self.base_distance),
            (self.active_locators[2], self.blend_locator, self.blend_distance),
            (self.active_locators[0], self.blend_locator, self.stretch_distance),
        ]

        for loc_start, loc_end, dist in connections:
            self._connect_distance(loc_start, loc_end, dist)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # STEP 4 : CONNECT THE DG NODES
        # General Connections
        # Connect static distances to static plus min to get limb length
        cmds.connectAttr(f"{self.static_distances[0]}.distance", f"{self.lenStatic_plusMin}.input1D[0]")
        cmds.connectAttr(f"{self.static_distances[1]}.distance", f"{self.lenStatic_plusMin}.input1D[1]")

        # Connect base and static distances to get the length scale
        cmds.connectAttr(f"{self.base_distance}.distance", f"{self.attrScaler_multDiv}.input1X")
        cmds.connectAttr(f"{self.static_distances[2]}.distance", f"{self.attrScaler_multDiv}.input2X")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Soft Connections
        # Connection to limb soft plus minus 1
        cmds.connectAttr(f"{self.lenStatic_plusMin}.output1D", f"{self.soft_plusMin_1}.input1D[0]")
        cmds.connectAttr(f"{self.controls[2]}.{role.SOFT}", f"{self.soft_plusMin_1}.input1D[1]")

        # Connection to limb soft scaler 1
        cmds.connectAttr(f"{self.active_distances[2]}.distance", f"{self.softScaler_multDiv}.input1X")
        cmds.connectAttr(f"{self.attrScaler_multDiv}.outputX", f"{self.softScaler_multDiv}.input2X")

        # Connection to limb soft plus minus 2
        cmds.connectAttr(f"{self.soft_plusMin_1}.output1D", f"{self.soft_plusMin_2}.input1D[1]")
        cmds.connectAttr(f"{self.softScaler_multDiv}.outputX", f"{self.soft_plusMin_2}.input1D[0]")

        # Connection to soft plus minus 4
        input1 = ".input1D[1]" if self.side_id == setup.MIRROR_SIDE_ID else ".input1D[0]"
        input2 = ".input1D[0]" if self.side_id == setup.MIRROR_SIDE_ID else ".input1D[1]"
        cmds.connectAttr(f"{self.soft_cond}.outColorR", f"{self.soft_plusMin_4}.{input1}")
        cmds.connectAttr(f"{self.softScaler_multDiv}.outputX", f"{self.soft_plusMin_4}{input2}")

        # Connection to limb soft multiply divide 1
        cmds.connectAttr(f"{self.controls[2]}.{role.SOFT}", f"{self.soft_multDiv_1}.input2X")
        cmds.connectAttr(f"{self.soft_plusMin_2}.output1D", f"{self.soft_multDiv_1}.input1X")

        # Connection to limb soft multiply divide 2
        cmds.connectAttr(f"{self.soft_multDiv_1}.outputX", f"{self.soft_multDiv_2}.input1X")

        # Connection to limb soft multiply divide 3
        cmds.connectAttr(f"{self.soft_multDiv_2}.outputX", f"{self.soft_multDiv_3}.input2X")

        # Connection to limb soft multiply divide 4
        cmds.connectAttr(f"{self.soft_multDiv_3}.outputX", f"{self.soft_multDiv_4}.input1X")
        cmds.connectAttr(f"{self.controls[2]}.{role.SOFT}", f"{self.soft_multDiv_4}.input2X")

        # Connection to limb soft plus minus 3
        cmds.connectAttr(f"{self.soft_multDiv_4}.outputX", f"{self.soft_plusMin_3}.input1D[1]")
        cmds.connectAttr(f"{self.lenStatic_plusMin}.output1D", f"{self.soft_plusMin_3}.input1D[0]")

        # Connection to limb soft condition
        cmds.connectAttr(f"{self.softScaler_multDiv}.outputX", f"{self.soft_cond}.colorIfFalseR")
        cmds.connectAttr(f"{self.soft_plusMin_3}.output1D", f"{self.soft_cond}.colorIfTrueR")
        cmds.connectAttr(f"{self.softScaler_multDiv}.outputX", f"{self.soft_cond}.firstTerm")
        cmds.connectAttr(f"{self.soft_plusMin_1}.output1D", f"{self.soft_cond}.secondTerm")

        # Connection to limb active locator
        cmds.connectAttr(f"{self.soft_multDiv_4}.outputX", f"{self.active_locators[2]}.translate{self.axis}")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Stretch Connections
        # Connection to limb stretch multiply divide 1
        cmds.connectAttr(f"{self.blend_distance}.distance", f"{self.stretchScaler_multDiv}.input1X")
        cmds.connectAttr(f"{self.attrScaler_multDiv}.outputX", f"{self.stretchScaler_multDiv}.input2X")

        # Connection to limb up stretch multiply divide 1
        cmds.connectAttr(f"{self.static_distances[0]}.distance", f"{self.stretch1_multDiv_1}.input1X")
        cmds.connectAttr(f"{self.lenStatic_plusMin}.output1D", f"{self.stretch1_multDiv_1}.input2X")

        # Connection to limb low stretch multiply divide 1
        cmds.connectAttr(f"{self.static_distances[1]}.distance", f"{self.stretch2_multDiv_1}.input1X")
        cmds.connectAttr(f"{self.lenStatic_plusMin}.output1D", f"{self.stretch2_multDiv_1}.input2X")

        # Connection to limb up stretch multiply divide 2
        cmds.connectAttr(f"{self.stretchScaler_multDiv}.outputX", f"{self.stretch1_multDiv_2}.input1X")
        cmds.connectAttr(f"{self.stretch1_multDiv_1}.outputX", f"{self.stretch1_multDiv_2}.input2X")

        # Connection to limb low stretch multiply divide 2
        cmds.connectAttr(f"{self.stretchScaler_multDiv}.outputX", f"{self.stretch2_multDiv_2}.input1X")
        cmds.connectAttr(f"{self.stretch2_multDiv_1}.outputX", f"{self.stretch2_multDiv_2}.input2X")

        # Connection to limb up stretch multiply divide 3
        cmds.connectAttr(f"{self.stretch1_multDiv_2}.outputX", f"{self.stretch1_multDiv_3}.input1X")
        cmds.connectAttr(f"{self.controls[2]}.{role.STRETCH}", f"{self.stretch1_multDiv_3}.input2X")

        # Connection to limb low stretch multiply divide 3
        cmds.connectAttr(f"{self.stretch2_multDiv_2}.outputX", f"{self.stretch2_multDiv_3}.input1X")
        cmds.connectAttr(f"{self.controls[2]}.{role.STRETCH}", f"{self.stretch2_multDiv_3}.input2X")

        # Connection to limb up stretch plus minus 1
        cmds.connectAttr(f"{self.static_distances[0]}.distance", f"{self.stretch1_plusMin_1}.input1D[1]")
        cmds.connectAttr(f"{self.stretch2_multDiv_3}.outputX", f"{self.stretch1_plusMin_1}.input1D[0]")

        # Connection to limb low stretch plus minus 1
        cmds.connectAttr(f"{self.static_distances[1]}.distance", f"{self.stretch2_plusMin_1}.input1D[1]")
        cmds.connectAttr(f"{self.stretch2_multDiv_3}.outputX", f"{self.stretch2_plusMin_1}.input1D[0]")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Hinge pin connections
        # Connection to limb up hinge pin multiply divide 1
        cmds.connectAttr(f"{self.active_distances[0]}.distance", f"{self.pinScaler1_multDiv}.input1X")
        cmds.connectAttr(f"{self.attrScaler_multDiv}.outputX", f"{self.pinScaler1_multDiv}.input2X")

        # Connection to limb low hinge pin multiply divide 1
        cmds.connectAttr(f"{self.active_distances[1]}.distance", f"{self.pinScaler2_multDiv}.input1X")
        cmds.connectAttr(f"{self.attrScaler_multDiv}.outputX", f"{self.pinScaler2_multDiv}.input2X")

        # Connection to limb up hinge pin blend 1
        cmds.connectAttr(f"{self.controls[2]}.{role.PIN}", f"{self.pin1_blend}.attributesBlender")
        cmds.connectAttr(f"{self.slide1_plusMin_2}.output1D", f"{self.pin1_blend}.input[0]")
        cmds.connectAttr(f"{self.pinScaler1_multDiv}.outputX", f"{self.pin1_blend}.input[1]")

        # Connection to limb up hinge pin blend 1
        cmds.connectAttr(f"{self.controls[2]}.{role.PIN}", f"{self.pin2_blend}.attributesBlender")
        cmds.connectAttr(f"{self.slide2_plusMin_2}.output1D", f"{self.pin2_blend}.input[0]")
        cmds.connectAttr(f"{self.pinScaler2_multDiv}.outputX", f"{self.pin2_blend}.input[1]")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Hinge slide connections
        # Connection to limb hinge slide scaler 1
        cmds.connectAttr(f"{self.active_distances[2]}.distance", f"{self.slideScaler3_multDiv}.input1X")
        cmds.connectAttr(f"{self.attrScaler_multDiv}.outputX", f"{self.slideScaler3_multDiv}.input2X")

        # Connection to limb hinge slide limiter 1
        cmds.connectAttr(f"{self.controls[2]}.{role.SLIDE}", f"{self.slideLimiter_multDiv}.input1X")

        # Connection to limb up hinge slide plus minus 1
        cmds.connectAttr(f"{self.slideScaler3_multDiv}.outputX", f"{self.slide1_plusMin_1}.input1D[0]")
        cmds.connectAttr(f"{self.stretch1_plusMin_1}.output1D", f"{self.slide1_plusMin_1}.input1D[1]")

        # Connection to limb low hinge slide plus minus 1
        cmds.connectAttr(f"{self.slideScaler3_multDiv}.outputX", f"{self.slide2_plusMin_1}.input1D[0]")
        cmds.connectAttr(f"{self.stretch2_plusMin_1}.output1D", f"{self.slide2_plusMin_1}.input1D[1]")

        # Connection to limb up hinge slide plus minus 2
        cmds.connectAttr(f"{self.stretch1_plusMin_1}.output1D", f"{self.slide1_plusMin_2}.input1D[0]")
        cmds.connectAttr(f"{self.slide_cond}.outColorR", f"{self.slide1_plusMin_2}.input1D[1]")

        # Connection to limb low hinge slide plus minus 2
        cmds.connectAttr(f"{self.stretch2_plusMin_1}.output1D", f"{self.slide2_plusMin_2}.input1D[0]")
        cmds.connectAttr(f"{self.slide_cond}.outColorR", f"{self.slide2_plusMin_2}.input1D[1]")

        # Connection to limb up hinge slide multiply divide 1
        cmds.connectAttr(f"{self.slide1_plusMin_1}.output1D", f"{self.slideScaler1_multDiv}.input1X")
        cmds.connectAttr(f"{self.slideLimiter_multDiv}.outputX", f"{self.slideScaler1_multDiv}.input2X")

        # Connection to limb low hinge slide multiply divide 1
        cmds.connectAttr(f"{self.slide2_plusMin_1}.output1D", f"{self.slideScaler2_multDiv}.input1X")
        cmds.connectAttr(f"{self.slideLimiter_multDiv}.outputX", f"{self.slideScaler2_multDiv}.input2X")

        # Connection to limb hinge slide condition 1
        cmds.connectAttr(f"{self.slideScaler2_multDiv}.outputX", f"{self.slide_cond}.colorIfFalseR")
        cmds.connectAttr(f"{self.slideScaler1_multDiv}.outputX", f"{self.slide_cond}.colorIfTrueR")
        cmds.connectAttr(f"{self.slideLimiter_multDiv}.outputX", f"{self.slide_cond}.firstTerm")

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # General Connections
        # Feature normalization
        cmds.connectAttr(f"{self.pin1_blend}.outputX", f"{self.normalize1_multDiv}.input1X")
        cmds.connectAttr(f"{self.pin2_blend}.outputX", f"{self.normalize2_multDiv}.input1X")

        # Limb joint connection
        cmds.connectAttr(f"{self.normalize1_multDiv}.outputX", f"{self.joints[1]}.translate{self.axis}")
        cmds.connectAttr(f"{self.normalize2_multDiv}.outputX", f"{self.joints[2]}.translate{self.axis}")

        # Blend Constraint
        blendConstraint = cmds.pointConstraint([self.controls[2], self.active_locators[2]], self.blend_locator)[0]
        cmds.connectAttr(f"{self.controls[2]}.{role.STRETCH}", f"{self.stretch_reverse}.input1X")
        cmds.connectAttr(f"{self.controls[2]}.{role.STRETCH}", f"{blendConstraint}.{self.controls[2]}WO")
        cmds.connectAttr(f"{self.stretch_reverse}.outputX", f"{blendConstraint}.{self.active_locators[2]}W1")
