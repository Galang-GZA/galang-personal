"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds

from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_limb.constant import *

from galang_utils.rigbuilder.modules.module_limb.guide import Limb_GuideInfo, Limb_GuideList
from galang_utils.rigbuilder.modules.module_limb.controls import Limb_ControlCreator
from galang_utils.rigbuilder.modules.module_limb.jointchain import Limb_JointChainSetup
from galang_utils.rigbuilder.modules.module_limb.kinematics import Limb_IKSetup, Limb_FKSetup

from galang_utils.rigbuilder.modules.module_hand.zpackage import *


class Limb_ModuleBuilder:
    def __init__(self, guide):
        self.guide = Limb_GuideInfo(guide)
        self.input = Limb_GuideList(guide)
        self.result_joint = Limb_JointChainSetup(guide, RESULT)
        self.fk = Limb_FKSetup(guide)
        self.ik = Limb_IKSetup(guide)
        self.limb_module_group = None
        self.limb_module_blend_map = {}
        self.limb_module_control = None

    def build(self):
        # Step 0: Create Module Group
        group_name = limb_level_format(PJ, self.guide.module, self.guide.side, self.guide.name_raw, GROUP, item=None)
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

                # Kinematic switcher
                self.limb_module_control = Limb_ControlCreator(g.name, MODULE)
                self.limb_module_control.create()

                #   Lock and hide oiriginal attributes
                attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "visibility"]
                for attr in attrs:
                    cmds.setAttr(f"{self.limb_module_control.ctrl}.{attr}", lock=True, keyable=False, channelBox=False)

                #   Create kinematic switch attribute
                if not cmds.attributeQuery(IKFKSWITCH, node=self.limb_module_control.ctrl, exists=True):
                    cmds.addAttr(
                        self.limb_module_control.ctrl, ln=IKFKSWITCH, at="double", min=0, max=1, dv=0, keyable=True
                    )
                    cmds.parent(self.limb_module_control.top, self.limb_module_group)
                    cmds.pointConstraint(result_joint, self.limb_module_control.top)
                    # cmds.scaleConstraint(result_joint, self.limb_module_control.top)

                kinematic_switch_attr = f"{self.limb_module_control.ctrl}.{IKFKSWITCH}"
                kinematic_switch_reverse = cmds.createNode(
                    "reverse", name=limb_level_format(PJ, MODULE, g.side, g.name_raw, level=None, item=REVERSE)
                )
                cmds.connectAttr(kinematic_switch_attr, f"{kinematic_switch_reverse}.inputX")
                cmds.connectAttr(kinematic_switch_attr, f"{self.fk.fk_module_group}.visibility")
                cmds.connectAttr(f"{kinematic_switch_reverse}.outputX", f"{self.ik.ik_module_group}.visibility")

                # Hand module
                if g.module == HAND:
                    self.hand_module_control = Hand_ModuleBuilder(g.name)

                    pass

            if not (result_joint and ik_data and fk_data):
                continue
            ik_joint = ik_data[JNT]
            fk_joint = fk_data[JNT]
            pairblend_name = limb_level_format(PJ, RESULT, g.side, g.name_raw, level=None, item=PAIRBLEND)
            blendcolor_name = limb_level_format(PJ, RESULT, g.side, g.name_raw, level=None, item=SCALEBLEND)
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
            cmds.connectAttr(f"{scale_blend}.output", f"{self.limb_module_control.top}.scale")

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
