import maya.cmds as cmds
from typing import List, Dict
from galang_utils.rigbuilder.guide import *
from galang_utils.rigbuilder.constants import *


class SideRenamer:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.input = GuideList(guide)
        self.mirror_plane = MIRROR_PLANE

    def side_rename(self):
        for joint in self.input.guides:
            if joint.side == (0):
                if not DEFAULT_CENTER == CENTER:
                    cmds.rename(joint.name, f"{CENTER}_{joint.name_raw}")
            if joint.side == (1):
                if not DEFAULT_LEFT == LEFT:
                    cmds.rename(joint.name, f"{LEFT}_{joint.name_raw}")
            if joint.side == (2):
                if not DEFAULT_RIGHT == RIGHT:
                    cmds.rename(joint.name, f"{RIGHT}_{joint.name_raw}")

    @staticmethod
    def run(guide):
        program = SideRenamer(guide)
        program.side_rename()
