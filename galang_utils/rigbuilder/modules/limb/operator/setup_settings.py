from maya import cmds
from galang_utils.rigbuilder.constants.project import role as role
from galang_utils.rigbuilder.constants.general import role as gen_role

from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat
from rigbuilder.modules.base.operator.dg import Node
from rigbuilder.modules.limb.component.setup_settings import LimbSettingComponent
from rigbuilder.modules.limb.component.zcomponents import LimbComponents


class LimbSettingOperator(LimbSettingComponent):
    def __init__(self, component: LimbComponents):
        super().__init__(component.module)

        # Pre computed dag components
        self.ik_group = component.ik.group
        self.fk_group = component.ik.group
        self.ik_controls = component.ik.controls
        self.fk_controls = component.fk.controls

        # Pre compute dg nodes
        self.reverse = Node(self.guide, component.module, [role.SETTINGS, role.REVERSE])

    def run(self):
        # STEP 0 : CONNECT SETTING CONTROL TO IK FK VISIBILITY
        cmds.connectAttr(f"{self.control}.{role.IKFKSWITCH}", f"{self.reverse}.inputX")
        cmds.connectAttr(f"{self.control}.{role.IKFKSWITCH}", f"{self.fk_group}.visibility")
        cmds.connectAttr(f"{self.reverse}.outputX", f"{self.ik_group}.visibility")

        # STEP 1 : PROXY ATTRIBUTE TO IK FK CONTROLS
        for i in range(len(self.guides)):
            controls = [self.ik_controls[i], self.fk_controls[i]]
            proxy = "%s.%s" % (self.control, role.IKFKSWITCH)

            for control in controls:
                cmds.addAttr(control, ln=role.KINEMATICS, at="enum", en="-", keyable=False)
                cmds.setAttr(f"{control}.{role.KINEMATICS}", e=True, cb=True)
                cmds.addAttr(control, proxy=proxy, ln=role.IKFKSWITCH, at="double", min=0, max=1, keyable=True)
