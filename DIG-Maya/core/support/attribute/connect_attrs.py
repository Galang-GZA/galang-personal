from typing import List
from maya import cmds


def run(source_node: str, source_attrs: List[str], target_node: str, target_attrs: List[str]):
    for source_attr, target_attr in zip(source_attrs, target_attrs):
        cmds.connectAttr(f"{source_node}.{source_attr}", f"{target_node}.{target_attr}")
