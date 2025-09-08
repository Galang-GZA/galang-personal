from typing import List
from maya import cmds


class Attributes:
    def __init__(self, object, exceptions: List[str] = None):
        self.keyable_attrs = cmds.listAttr(object, k=True)
        self.resolved_attrs = list(set(self.keyable_attrs) - set(exceptions))

    def lock_and_hide(self):
        for attr in self.resolved_attrs:
            cmds.setAttr(f"{object}.{attr}", lock=True, keyable=False, channelBox=False)
