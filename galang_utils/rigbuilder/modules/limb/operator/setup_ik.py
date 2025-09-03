from maya import cmds
from typing import List

from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup
from rigbuilder.constants.general import role as gen_role

from rigbuilder.modules.base.operator.dg import Node
from rigbuilder.modules.base.operator.distance import DistanceNode, DistanceSet
from rigbuilder.modules.limb.component.zcomponent import LimbComponent


class LimbIKOperator:
    def __init__(self, component: LimbComponent):
        self.module = component.module
        self.axis = self.module.axis
        self.side_id = self.module.side_id
        self.guides = component.ik.guides
        self.control_guides = component.ik.control_guides

        # Pre compute dag components
        self.joints = component.ik.joints
        self.controls = component.ik.controls
        self.handle = component.ik.handle

        self.static_locators = component.ik.static_locators
        self.active_locators = component.ik.active_locators
        self.stretch_locator = component.ik.stretch_locator
        self.base_locator = component.ik.base_locator
        self.blend_locator = component.ik.blend_locator

        # Pre compute dg components
        self.static_distances = DistanceSet(self.guides, self.module, [role.IK, role.STATIC])
        self.active_distances = DistanceSet(self.control_guides, self.module, [role.IK, role.ACTIVE])
        self.base_distance = DistanceNode(self.control_guides[2], self.module, [role.IK, role.ACTIVE, role.BASE])
        self.blend_distance = DistanceNode(self.control_guides[2], self.module, [role.IK, role.ACTIVE, role.BLEND])
        self.stretch_distance = DistanceNode(self.control_guides[2], self.module, [role.IK, role.ACTIVE, role.STRETCH])

        # Pre compute math dg components
        # Argument for node types
        reverse = [role.IK, gen_role.REVERSE]
        reverse_stretch: List = reverse.append(role.STRETCH)

        blend = [role.IK, gen_role.BLEND]
        blend_pin: List = blend.append(role.PIN)

        mult_div = [role.IK, gen_role.MULT_DIV]
        mult_div_pin: List = mult_div.append(role.PIN)
        mult_div_attr: List = mult_div.append(role.ATTR)
        mult_div_soft: List = mult_div.append(role.SOFT)
        mult_div_slide: List = mult_div.append(role.SLIDE)
        mult_div_normal: List = mult_div.append(role.NORMAL)
        mult_div_stretch: List = mult_div.append(role.STRETCH)
        mult_div_pin_scaler: List = mult_div_pin.append(role.SCALER)
        mult_div_soft_scaler: List = mult_div_soft.append(role.SCALER)
        mult_div_attr_scaler: List = mult_div_attr.append(role.SCALER)
        mult_div_slide_scaler: List = mult_div_slide.append(role.SCALER)
        mult_div_stretch_scaler: List = mult_div_stretch.append(role.SCALER)
        mult_div_slide_limiter: List = mult_div_slide.append(role.LIMITER)

        plus_min = [role.IK, gen_role.PLUS_MIN]
        plus_min_soft: List = plus_min.append(role.SOFT)
        plus_min_slide: List = plus_min.append(role.SLIDE)
        plus_min_stretch: List = plus_min.append(role.STRETCH)
        plus_min_static: List = plus_min.append(role.STATIC)
        plus_min_active: List = plus_min.append(role.ACTIVE)

        condition = [role.IK, gen_role.CONDITION]
        condition_soft: List = condition.append(role.SOFT)
        condition_slide: List = condition.append(role.SLIDE)

        # Normalization math nodes
        self.normalize1_multDiv = Node(self.guides[0], self.module, mult_div_normal)
        self.normalize2_multDiv = Node(self.guides[1], self.module, mult_div_normal)

        # Chain Len math nodes
        self.lenStatic_plusMin = Node(self.guides[2], self.module, plus_min_static)
        self.LenActive_plusMin = Node(self.guides[2], self.module, plus_min_active)

        # Setup soft math nodes
        self.soft_cond = Node(self.guides[2], self.module, condition_soft)
        self.soft_plusMin_1 = Node(self.guides[2], self.module, plus_min_soft.append(1))
        self.soft_plusMin_2 = Node(self.guides[2], self.module, plus_min_soft.append(2))
        self.soft_plusMin_3 = Node(self.guides[2], self.module, plus_min_soft.append(3))
        self.soft_plusMin_4 = Node(self.guides[2], self.module, plus_min_soft.append(4))
        self.soft_multDiv_1 = Node(self.guides[2], self.module, mult_div_soft.append(1))
        self.soft_multDiv_2 = Node(self.guides[2], self.module, mult_div_soft.append(2))
        self.soft_multDiv_3 = Node(self.guides[2], self.module, mult_div_soft.append(3))
        self.soft_multDiv_4 = Node(self.guides[2], self.module, mult_div_soft.append(4))
        self.softScaler_multDiv = Node(self.guides[2], self.module, mult_div_soft_scaler)
        self.attrScaler_multDiv = Node(self.guides[2], self.module, mult_div_attr_scaler)

        # Setup stretch math nodes
        self.stretch1_plusMin_1 = Node(self.guides[0], self.module, plus_min_stretch.append(1))
        self.stretch2_plusMin_1 = Node(self.guides[1], self.module, plus_min_stretch.append(1))
        self.stretch1_multDiv_1 = Node(self.guides[0], self.module, mult_div_stretch.append(1))
        self.stretch1_multDiv_2 = Node(self.guides[0], self.module, mult_div_stretch.append(2))
        self.stretch1_multDiv_3 = Node(self.guides[0], self.module, mult_div_stretch.append(3))
        self.stretch2_multDiv_1 = Node(self.guides[1], self.module, mult_div_stretch.append(1))
        self.stretch2_multDiv_2 = Node(self.guides[1], self.module, mult_div_stretch.append(2))
        self.stretch2_multDiv_3 = Node(self.guides[1], self.module, mult_div_stretch.append(3))
        self.stretchScaler_multDiv = Node(self.guides[2], self.module, mult_div_stretch_scaler)

        # Setup pin math nodes
        self.pin1_blend = Node(self.guides[0], self.module, blend_pin)
        self.pin2_blend = Node(self.guides[1], self.module, blend_pin)
        self.pinScaler1_multDiv = Node(self.guides[0], self.module, mult_div_pin_scaler)
        self.pinScaler2_multDiv = Node(self.guides[1], self.module, mult_div_pin_scaler)

        # Setup slide math nodes
        self.slide_cond = Node(self.guides[2], self.module, condition_slide)
        self.slide1_plusMin_1 = Node(self.guides[0], self.module, plus_min_slide.append(1))
        self.slide1_plusMin_2 = Node(self.guides[0], self.module, plus_min_slide.append(2))
        self.slide2_plusMin_1 = Node(self.guides[1], self.module, plus_min_slide.append(1))
        self.slide2_plusMin_2 = Node(self.guides[1], self.module, plus_min_slide.append(2))
        self.slideScaler1_multDiv = Node(self.guides[0], self.module, mult_div_slide_scaler)
        self.slideScaler2_multDiv = Node(self.guides[1], self.module, mult_div_slide_scaler)
        self.slideScaler3_multDiv = Node(self.guides[2], self.module, mult_div_slide_scaler)
        self.slideLimiter_multDiv = Node(self.guides[2], self.module, mult_div_slide_limiter)

        # Setup blend math nodes
        self.stretch_reverse = Node(self.guides[3], self.module, reverse_stretch)

    def _connect_distance(self, loc_start: str, loc_end: str, dist: str):
        cmds.connectAttr(f"{loc_start}.worldPosition[0]", f"{dist}.startPoint", force=True)
        cmds.connectAttr(f"{loc_end}.worldPosition[0]", f"{dist}.endPoint", force=True)

    def run(self):
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # STEP 0 : CREATE PRE COMPUTED DG COMPONENTS
        # Create distance nodes
        components: List[Node] = [
            self.static_distances,
            self.active_distances,
            self.base_distance,
            self.blend_distance,
            self.stretch_distance,
        ]
        for component in components:
            component.create()

        # Create normalization math nodes
        self.normalize1_multDiv.create({"input2X": -1.0 if self.side_id == setup.MIRROR_SIDE_ID else 1.0})
        self.normalize2_multDiv.create({"input2X": -1.0 if self.side_id == setup.MIRROR_SIDE_ID else 1.0})

        # Create chain Len math nodes
        self.lenStatic_plusMin.create({"operation": 1})
        self.LenActive_plusMin.create({"operation": 1})

        # Create soft math nodes
        self.soft_plusMin_1.create({"operation": 2})
        self.soft_plusMin_2.create({"operation": 2})
        self.soft_plusMin_3.create({"operation": 2})
        self.soft_plusMin_4.create({"operation": 2})
        self.soft_multDiv_1.create({"operation": 2})
        self.soft_multDiv_2.create({"input2X": -1.0})
        self.soft_multDiv_3.create({"operation": 3, "input1X": 2.718})
        self.soft_multDiv_4.create()
        self.softScaler_multDiv.create({"operation": 2})
        self.attrScaler_multDiv.create({"operation": 2})
        self.soft_cond.create({"operation": 2})

        # Create stretch math nodes
        self.stretch1_plusMin_1.create({"operation": 1})
        self.stretch2_plusMin_1.create({"operation": 1})
        self.stretch1_multDiv_1.create({"operation": 2})
        self.stretch1_multDiv_2.create()
        self.stretch1_multDiv_3.create()
        self.stretch2_multDiv_1.create({"operation": 2})
        self.stretch2_multDiv_2.create()
        self.stretch2_multDiv_3.create()
        self.stretchScaler_multDiv.create({"operation": 2})

        # Create pin math nodes
        self.pinScaler1_multDiv.create({"operation": 2})
        self.pinScaler2_multDiv.create({"operation": 2})
        self.pin1_blend.create()
        self.pin2_blend.create()

        # Create slide math nodes
        self.slide1_plusMin_1.create({"operation": 2})
        self.slide1_plusMin_2.create({"operation": 2})
        self.slide2_plusMin_1.create({"operation": 2})
        self.slide2_plusMin_2.create({"operation": 2})
        self.slide_cond.create({"operation": 2})
        self.slideScaler1_multDiv.create()
        self.slideScaler2_multDiv.create()
        self.slideScaler3_multDiv.create({"operation": 2})
        self.slideLimiter_multDiv.create()

        # Create blend math nodes
        self.stretch_reverse.create()

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
        cmds.connectAttr(f"{self.soft_multDiv_4}.output1D", f"{self.active_locators[2]}.translate{self.axis}")

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
        cmds.connectAttr(f"{self.active_distances}.distance", f"{self.slideScaler3_multDiv}.input1X")
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
        cmds.connectAttr(f"{self.pin1_blend}.outputX", f"{self.normalize1_multDiv}.input1")
        cmds.connectAttr(f"{self.pin2_blend}.outputX", f"{self.normalize1_multDiv}.input1")

        # Limb joint connection
        cmds.connectAttr(f"{self.normalize1_multDiv}.outputX", f"{self.joints[1]}.translate{self.axis}")
        cmds.connectAttr(f"{self.normalize2_multDiv}.outputX", f"{self.joints[2]}.translate{self.axis}")

        # Blend Constraint
        BlendConstraint = cmds.pointConstraint([self.controls[2], self.active_locators[2]], self.blend_locator)[0]
        cmds.connectAttr(f"{self.controls[2]}.{role.STRETCH}", f"{self.stretch_reverse}.input1X")
        cmds.connectAttr(f"{self.controls[2]}.{role.STRETCH}", f"{BlendConstraint}.{self.controls[2]}WO")
        cmds.connectAttr(f"{self.stretch_reverse}.outputX", f"{BlendConstraint}.{self.active_locators[2]}W1")
