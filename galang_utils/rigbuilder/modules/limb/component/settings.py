from maya import cmds

from galang_utils.rigbuilder.constant.project import role as P_ROLE

from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.limb.program.control import LimbControlCreator


class LimbSettingComponent:
    def __init__(self, module: ModuleInfo):
        self.module = module
        self.control: LimbControlCreator = None

    def create(self):
        limb_setting = self.module.guides_end[0]
        self.setting = LimbControlCreator(limb_setting, P_ROLE.SETTINGS, self.module)
        self.setting.create()

        #   Lock and hide oiriginal attributes
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "visibility"]
        for attr in attrs:
            cmds.setAttr(f"{self.setting.ctrl}.{attr}", lock=True, keyable=False, channelBox=False)

        #   Create kinematic switch attribute
        if not cmds.attributeQuery(P_ROLE.IKFKSWITCH, node=self.setting.ctrl, exists=True):
            cmds.addAttr(self.setting.ctrl, ln=P_ROLE.IKFKSWITCH, at="double", min=0, max=1, dv=0, keyable=True)
