from maya import cmds
from typing import List, Dict
from rigbuilder.constants.project import role as role
from rigbuilder.constants.project import setup as setup
from rigbuilder.cores.guide import GuideInfo, ModuleInfo
from rigbuilder.modules.base.constant.format import Format


class Node(str):
    def __new__(cls, guide: GuideInfo, module: ModuleInfo, types: List):
        format = Format(module.side)
        name = format.name(guide.name_raw, types)
        return super().__new__(cls, name)

    def __init__(self, guide: GuideInfo, module: ModuleInfo, types: List):
        self.types = types
        self.guide = guide
        self.module = module

    def create(self, attributes: Dict = None):
        # Create Node
        types_order = []
        type = next((item for item in types_order if item in self.types), None)
        node = cmds.createNode(self.types[0], n=self)

        # Set attributes
        if attributes:
            for attribute, value in attributes.items():
                cmds.setAttr(f"{node}.{attribute}", value)

        return node

    def run(self):
        pass
