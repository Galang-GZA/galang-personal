from typing import Dict, List
from RigXFrame.core.guide import ModuleInfo
from core.component.joint import JointSet


class BindComponent:
    def __init__(self, module: ModuleInfo):
        self.guide = module.guide
        self.joints = JointSet(self.guide.name, create_group=False)

    def create(self):
        self.__create_bind_components()

    def __create_bind_components(self):
        # # STEP 0 : CREATE PRE COMPUTED COMPONENTS
        self.joints.create
