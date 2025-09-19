import maya.cmds as cmds
from typing import List, Dict
from galang_utils.rig_x_frame.guide import *
from galang_utils.rig_x_frame.constants import *


class JointMirror:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.input = GuideList(guide)
        self.mirror_plane = MIRROR_PLANE

    def mirror_joint(self):
        # Check side
        if self.guide.side_id in (0, 3):
            result = cmds.confirmDialog(
                title="Side Mismatch",
                message="This side doesn't seem to be mirrored thoooo. Want me to set this side?",
                button=["Yes, side Left", "Yes, side Right", "Hol Up, lemme check"],
                defaultButton="Yes, side Left",
                cancelButton="Hol up, lemme check",
                dismissString="Hol up, lemme check",
            )
            if result == "Yes, side Left":
                cmds.setAttr(f"{self.guide.name}.side", 1)
                self.guide.side_id = 1
            elif result == "Yes, side Right":
                cmds.setAttr(f"{self.guide.name}.side", 2)
                self.guide.side_id = 1
            else:
                return

        # Determine side
        side_map = {1: (f"{LEFT}_", f"{RIGHT}_", 2), 2: (f"{RIGHT}_", f"{LEFT}_", 1)}
        self.search, self.replace, self.side_id_other = side_map.get(self.guide.side_id)

        # Determine the mirror plane
        plane_map = {"XY": (True, False, False), "XZ": (False, True, False), "YZ": (False, False, True)}
        self.planeXY, self.planeXZ, self.planeYZ = plane_map.get(self.mirror_plane)

        # check if mirrored already exist
        mirrored_name = self.guide.name.replace(self.search, self.replace)
        if cmds.objExists(mirrored_name):
            result = cmds.confirmDialog(
                title="Side Mirrored Already",
                message=f"Mirrored joint {mirrored_name} already exists. Want me to delete that bad boy and continue?",
                button=["Yes. Execute order 66", "Hol up, lemme check"],
                defaultButton="Yes. Execute order 66",
                cancelButton="Hol up, lemme check",
                dismissString="Hol up, lemme check",
            )
            if result == "Yes. Execute order 66":
                cmds.delete(mirrored_name)
            else:
                return

        # Check if there is any different side in hierarchy and change them
        for joint in self.input.guides:
            if not joint.side_id == self.guide.side_id:
                cmds.setAttr(f"{joint.name}.side", self.guide.side_id)

        # Mirror this bish
        mirrored_joint_chain = cmds.mirrorJoint(
            self.guide.name,
            mirrorBehavior=True,
            mxy=self.planeXY,
            mxz=self.planeXY,
            myz=self.planeXY,
            searchReplace=(self.search, self.replace),
        )
        for joint in mirrored_joint_chain:
            cmds.setAttr(f"{joint}.side", self.side_id_other)

    @staticmethod
    def run(guide):
        program = JointMirror(guide)
        program.mirror_joint()
