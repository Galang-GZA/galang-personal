from typing import List
from maya import cmds


def run(dag_name: str, attr_exceptions: List[str] = None):
    keyable_attrs = cmds.listAttr(dag_name, k=True)
    resolved_attrs = list(set(keyable_attrs) - set(attr_exceptions))
    for attr in resolved_attrs:
        cmds.setAttr(f"{dag_name}.{attr}", lock=True, keyable=False, channelBox=False)
