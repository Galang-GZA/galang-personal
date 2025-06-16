from maya import cmds
from typing import List, Dict, Union
from galang_utils.curve.shapes_library import *
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.guides.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.constant.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.base.controls import LimbControlCreator
from galang_utils.rigbuilder.modules.module_limb.base.jointchain import LimbJointChainSetup

from galang_utils.rigbuilder.modules.module_limb.component.bind import LimbBindComponent
from galang_utils.rigbuilder.modules.module_limb.component.fk import LimbFKComponent
from galang_utils.rigbuilder.modules.module_limb.component.ik import LimbIKComponent
from galang_utils.rigbuilder.modules.module_limb.component.result import LimbResultComponent
from galang_utils.rigbuilder.modules.module_limb.component.settings import LimbSettingComponent


class LimbComponent:
    def __init__(self, guide):
        self.bind = LimbBindComponent(guide)
        self.fk = LimbFKComponent(guide)
        self.ik = LimbIKComponent(guide)
        self.result = LimbResultComponent(guide)
        self.setting = LimbSettingComponent(guide)

    def create_bind(self):
        self.bind.create()
        self.fk.create()
        self.ik.create()
        self.result.create()
        self.setting.create()
