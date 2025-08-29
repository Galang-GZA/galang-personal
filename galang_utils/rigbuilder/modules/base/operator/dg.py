from maya import cmds
from typing import List
from galang_utils.rigbuilder.modules.limb.constant.format import LimbFormat


class Node:
    def __init__(self, side, kinematics=None):
        self.format = LimbFormat(side, kinematics)

    def setup(self, guide_name_raw=None, types: List = None, attributes: List = None, values: List = None):
        # Create Node
        node = cmds.createNode(type, n=self.format.name(guide_name_raw, types))

        # Set attributes
        if attributes and values:
            for attribute, value in zip(attributes, values):
                cmds.setAttr(f"{node}.{attribute}", value)

        return node
