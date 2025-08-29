from maya import cmds
from typing import Dict
from galang_utils.rigbuilder.constant.constant_general import *
from galang_utils.rigbuilder.constant.constant_project import *
from galang_utils.rigbuilder.modules.base.rule.constant_module import *
from rigbuilder.modules.base.component.z_component import *


class BaseBindOperator:
    def __init__(self, component: BaseComponent):
        self.component = component
        self.module = component.bind.module
        self.map: Dict = {}

    def run(self):
        bind_map = self.component.bind.map
        connection_map = self.component.bind_connection
        for guide in self.module.guides + self.module.guides_end:
            bind_jnt = bind_map.get(guide.name)
            connection_jnt = connection_map.get(guide.name)
            cmds.parentConstraint(connection_jnt, bind_jnt)
            cmds.scaleConstraint(connection_jnt, bind_jnt)
