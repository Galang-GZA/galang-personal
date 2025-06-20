from maya import cmds
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.guides.guide import ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.constant.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.base.controls import LimbControlCreator


class LimbSettingComponent:
    def __init__(self, guide):
        self.module = ModuleInfo(guide)
        self.setting = None

    def create(self):
        limb_setting = self.module.guides_end[0]
        self.setting = LimbControlCreator(limb_setting, SETTINGS, self.module)
        self.setting.create()

        #   Lock and hide oiriginal attributes
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "visibility"]
        for attr in attrs:
            cmds.setAttr(f"{self.setting.ctrl}.{attr}", lock=True, keyable=False, channelBox=False)

        #   Create kinematic switch attribute
        if not cmds.attributeQuery(IKFKSWITCH, node=self.setting.ctrl, exists=True):
            cmds.addAttr(self.setting.ctrl, ln=IKFKSWITCH, at="double", min=0, max=1, dv=0, keyable=True)
