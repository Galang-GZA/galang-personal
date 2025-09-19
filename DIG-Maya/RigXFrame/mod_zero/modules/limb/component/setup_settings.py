from maya import cmds

from galang_utils.rig_x_frame.constants.project import role as role
from rig_x_frame.programs.attr.configuration import Attributes

from galang_utils.rig_x_frame.core.guide import ModuleInfo
from galang_utils.rig_x_frame.mod_zero.base.component.group import GroupNode
from galang_utils.rig_x_frame.mod_zero.base.component.control import ControlNode


class LimbSettingComponent:
    def __init__(self, module: ModuleInfo):
        self.guides = module.guides
        self.guide = self.guides[-1]
        self.group = GroupNode(self.guide, module, [role.SETTINGS, role.RIG, role.GROUP])
        self.control = ControlNode(self.guide, module, role.SETTINGS)

    def create(self):
        self.control.create()

        #   Lock and hide oiriginal attributes
        Attributes(self.control).lock_and_hide()

        #   Create kinematic switch attribute
        if not cmds.attributeQuery(role.IKFKSWITCH, node=self.control, exists=True):
            cmds.addAttr(self.control, ln=role.IKFKSWITCH, at="double", min=0, max=1, dv=0, keyable=True)
