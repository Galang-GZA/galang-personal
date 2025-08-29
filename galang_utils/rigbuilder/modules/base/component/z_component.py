from typing import List
from galang_utils.rigbuilder.core.guide import ModuleInfo
from galang_utils.rigbuilder.modules.base.component.bind import BaseBindComponent
from rigbuilder.modules.base.component.fk_setup import BaseFKComponent


class BaseComponent:
    def __init__(self, module: ModuleInfo):
        self.bind = BaseBindComponent(module)
        self.fk = BaseFKComponent(module)
        self.bind_connection: List = []

    def create_bind(self):
        self.bind.create()

    def create_rig(self):
        self.fk.create()

        # Add result joints to bind connection
        self.bind_connection = self.fk.joints
