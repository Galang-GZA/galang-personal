from maya import cmds
from galang_utils.rigbuilder.constants.project import role as role
from galang_utils.rigbuilder.constants.general import role as gen_role

from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat
from galang_utils.rigbuilder.modules.limb.component.zcomponent import LimbComponent


class LimbSettingOperator:
    def __init__(self, component: LimbComponent):
        self.guide = component.module.guide
        self.guides = component.module.guides
        self.set_control = component.setting.control
        self.ik_top_group = component.ik.groups.get(role.TOP)
        self.fk_top_group = component.fk.groups.get(role.TOP)
        self.ik_joints = component.ik.joints
        self.ik_controls = component.ik.controls
        self.fk_joints = component.fk.joints
        self.fk_controls = component.fk.controls
        self.result_joints = component.result.joints
        self.pair_blends = component.result.pair_blends
        self.scale_blends = component.result.scale_blends
        self.format = LimbFormat(self.guide.side)

    def run(self):
        kinematics_switch_attr = f"{self.set_control}.{role.IKFKSWITCH}"
        kinematics_switch_reverse = cmds.createNode(
            "reverse", name=self.format.name(self.guide.name_raw, role.SETTINGS, role.REVERSE)
        )
        cmds.connectAttr(kinematics_switch_attr, f"{kinematics_switch_reverse}.inputX")
        cmds.connectAttr(kinematics_switch_attr, f"{self.fk_top_group}.visibility")
        cmds.connectAttr(f"{kinematics_switch_reverse}.outputX", f"{self.ik_top_group}.visibility")

        for i in range(len(self.guides)):
            cmds.connectAttr(kinematics_switch_attr, f"{self.pair_blends[i]}.weight", force=True)
            cmds.connectAttr(kinematics_switch_attr, f"{self.scale_blends[i]}.blender", force=True)

            controls = [self.ik_controls[i], self.fk_controls[i]]
            proxy = "%s.%s" % (self.set_control, role.IKFKSWITCH)

            for control in controls:
                cmds.addAttr(control.ctrl, ln=role.KINEMATICS, at="enum", en="-", keyable=False)
                cmds.setAttr(f"{control.ctrl}.{role.KINEMATICS}", e=True, cb=True)
                cmds.addAttr(control.ctrl, proxy=proxy, ln=role.IKFKSWITCH, at="double", min=0, max=1, keyable=True)

            if i == 2:
                cmds.scaleConstraint(self.result_joints[i], self.set_control.get_node(role.LINK))
                cmds.parentConstraint(self.result_joints[i], self.set_control.get_node(role.LINK))
