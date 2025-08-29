from maya import cmds

from galang_utils.rigbuilder.constant.project import role as role

from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.base.component.control import ControlNode


class LimbSettingComponent:
    def __init__(self, module: ModuleInfo):
        self.guide = module.guides[-1]
        self.control = ControlNode(self.guide, module, role.SETTINGS)

    def create(self):
        self.control.create()

        #   Lock and hide oiriginal attributes
        """ BIKIN UTILS UNTUK INI, BAKAL SERING DIPAKE"""
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "visibility"]
        for attr in attrs:
            cmds.setAttr(f"{self.control}.{attr}", lock=True, keyable=False, channelBox=False)

        #   Create kinematic switch attribute
        if not cmds.attributeQuery(role.IKFKSWITCH, node=self.control, exists=True):
            cmds.addAttr(self.control, ln=role.IKFKSWITCH, at="double", min=0, max=1, dv=0, keyable=True)
