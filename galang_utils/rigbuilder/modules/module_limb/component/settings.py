from maya import cmds
from typing import List, Dict, Union
from galang_utils.curve.shapes_library import *
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.guides.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.constant.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.base.controls import LimbControlCreator


class LimbSettingComponent:
    def __init__(self, guide):
        self.module = ModuleInfo(guide)
        self.setting = None

    def create(self):
        guide_setting = self.module.guides[0]
        self.setting = LimbControlCreator(guide_setting.name, MODULE)
        self.setting.create()

        #   Lock and hide oiriginal attributes
        attrs = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "visibility"]
        for attr in attrs:
            cmds.setAttr(f"{self.setting.ctrl}.{attr}", lock=True, keyable=False, channelBox=False)

        #   Create kinematic switch attribute
        if not cmds.attributeQuery(IKFKSWITCH, node=self.setting.ctrl, exists=True):
            cmds.addAttr(self.setting.ctrl, ln=IKFKSWITCH, at="double", min=0, max=1, dv=0, keyable=True)
