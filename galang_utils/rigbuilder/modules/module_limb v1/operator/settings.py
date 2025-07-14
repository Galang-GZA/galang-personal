from maya import cmds
from typing import Dict
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_limb.rule.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.component.zcomponent import *


class LimbSettingOperator:
    def __init__(self, component: LimbComponent):
        self.component = component
        self.module = component.setting.module

    def run(self):
        guide = self.module.guide
        setting_control = self.component.setting.setting.ctrl
        ik_group = self.component.ik.groups.get(MASTER)
        fk_group = self.component.fk.groups.get(MASTER)
        ik_map = self.component.ik.map
        fk_map = self.component.fk.map
        result_map = self.component.result.map

        kinematic_switch_attr = f"{setting_control}.{IKFKSWITCH}"
        kinematic_switch_reverse = cmds.createNode(
            "reverse", name=limb_level_format(PROJECT, MODULE, guide.side, guide.name_raw, level=None, item=REVERSE)
        )
        cmds.connectAttr(kinematic_switch_attr, f"{kinematic_switch_reverse}.inputX")
        cmds.connectAttr(kinematic_switch_attr, f"{fk_group}.visibility")
        cmds.connectAttr(f"{kinematic_switch_reverse}.outputX", f"{ik_group}.visibility")

        for index, guide in enumerate(self.module.guides + self.module.guides_end):
            ik_control = ik_map[guide.name][CTRL]
            fk_control = fk_map[guide.name][CTRL]
            pair_blend = result_map[guide.name][PAIRBLEND]
            scale_blend = result_map[guide.name][SCALEBLEND]

            cmds.connectAttr(kinematic_switch_attr, f"{pair_blend}.weight", force=True)
            cmds.connectAttr(kinematic_switch_attr, f"{scale_blend}.blender", force=True)

            controls = [ik_control, fk_control]
            proxy = "%s.%s" % (setting_control, IKFKSWITCH)

            for control in controls:
                cmds.addAttr(control.ctrl, ln=KINEMATICS, at="enum", en="-", keyable=False)
                cmds.setAttr(f"{control.ctrl}.{KINEMATICS}", e=True, cb=True)

            for control in controls:
                cmds.addAttr(control.ctrl, proxy=proxy, ln=IKFKSWITCH, at="double", min=0, max=1, keyable=True)

            if index == 2:
                result_joint = result_map[guide.name][JNT]
                cmds.scaleConstraint(result_joint, self.component.setting.setting.get_node(LINK))
                cmds.parentConstraint(result_joint, self.component.setting.setting.get_node(LINK))
