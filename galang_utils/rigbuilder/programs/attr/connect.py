from typing import List
from maya import cmds


class DNG_ConnectAttrs:
    def __init__(self, source_node, source_attrs: List, target_node, target_attr: List):
        self.keyable_attrs = cmds.listAttr(object, k=True)
        self.resolved_attrs = list(set(self.keyable_attrs) - set(exceptions))

    def run(self):
        for attr in self.resolved_attrs:
            cmds.setAttr(f"{object}.{attr}", lock=True, keyable=False, channelBox=False)
