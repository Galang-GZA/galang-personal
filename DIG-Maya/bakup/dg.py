from maya import cmds
from typing import List, Dict
from rig_x_frame.constants.project import role as role
from rig_x_frame.constants.project import setup as setup
from rig_x_frame.core.guide import GuideInfo, ModuleInfo
from rig_x_frame.mod_zero.base.constant.format import Format


class Node(str):
    def __new__(cls, guide: GuideInfo, module: ModuleInfo, types: List):
        format = Format(module.side)
        name = format.name(guide.name_raw, types)
        return super().__new__(cls, name)

    def __init__(self, guide: GuideInfo, module: ModuleInfo, types: List, attrs: Dict):
        self.types = types
        self.guide = guide
        self.module = module
        self.attributes = attrs

    def run(self):
        # Create Node
        types_order = []
        node_type = next((item for item in types_order if item in self.types), None)
        node = cmds.createNode(node_type, n=self)

        # Set attributes
        if self.attributes:
            for attr, value in self.attributes.items():
                cmds.setAttr(f"{node}.{attr}", value)

        return node


class NodeSet(List[Node]):
    def __init__(self, guides: List[GuideInfo], module: ModuleInfo, types: List, attrs: List[Dict]):
        for i in range(len(guides)):
            i = f"{i+1:02d}"
            resolved_types = [(i if t is setup.INDEX else t) for t in types]
            dg_node = Node(guides[i], module, [resolved_types])
            self.append(dg_node)

    def run(self):
        for dg_node in self:
            dg_node.run()
