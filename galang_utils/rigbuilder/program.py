import maya.cmds as cmds
from galang_utils.rigbuilder.guide import *
from galang_utils.rigbuilder.constant import *


class GuideReorient:
    def __init__(self, root_joint):
        self.input_guides = GuideList()
        self.input_guides.get_guides(root_joint)

    def joint_reorient(self):
        joint_to_reorient = [guide for guide in self.input_guides.guides if guide.module_start]
        module_locator = []

        for joint in joint_to_reorient:
            locator = cmds.spaceLocator(n=f"{joint}_Loc", p=(0, 0, 0))  # Create the locator
            locator = locator[0]
            cmds.xform(locator, t=joint.position, ro=joint.orientation, ws=True)  # Position the locator the bind joint
            cmds.parent(joint.name, locator)  # Parent the joint to the locator
            module_locator.append(locator)

        for joint, locator in zip(joint_to_reorient, module_locator):
            cmds.xform(locator, ws=True, t=(0, 0, 0), ro=(0, 0, 0))  # Position the locator to the world origin
            cmds.joint(
                joint.name, e=True, oj="xyz", secondaryAxisOrient="yup", ch=True, zso=True
            )  # Orient the bind joint

            joint_end = cmds.listRelatives(joint.name, allDescendents=True, type="joint")
            if joint_end:
                joint_end = joint_end[0]
                cmds.joint(joint_end, e=True, oj="none")  # Orient the end joint to the parent/world

            cmds.xform(
                locator, t=joint.position, ro=joint.orientation, ws=True
            )  # Position back the locator to the original joint's position
            if joint.parent:
                cmds.parent(joint.name, joint.parent)  # Parent the bind joint back to its original parent
            else:
                cmds.parent(joint.name, w=True)

            cmds.delete(locator)  # Delete the locator

    @staticmethod
    def run(root_joint):
        program = GuideReorient(root_joint)
        program.joint_reorient()


class Tools:
    def __init__(self, guide):
        guide_info = GuideInfo(guide)
        self.joint_chain = GuideList()
        self.joint_chain.get_guides(guide_info.name)
        self.name = guide_info.name
        self.side_id = guide_info.side_id
        self.mirror_plane = MIRROR_PLANE

    def side_rename(self):
        for joint in self.joint_chain.guides:
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
    def run_side_rename(guide):
        program = Tools(guide)
        program.side_rename()

    def mirror_joint(self):
        # Check side
        if self.side_id in (0, 3):
            result = cmds.confirmDialog(
                title="Side Mismatch",
                message="This side doesn't seem to be mirrored thoooo. Want me to set this side?",
                button=["Yes, side Left", "Yes, side Right", "Hol Up, lemme check"],
                defaultButton="Yes, side Left",
                cancelButton="Hol up, lemme check",
                dismissString="Hol up, lemme check",
            )
            if result == "Yes, side Left":
                cmds.setAttr(f"{self.name}.side", 1)
                self.side_id = 1
            elif result == "Yes, side Right":
                cmds.setAttr(f"{self.name}.side", 2)
                self.side_id = 1
            else:
                return

        # Determine side
        side_map = {1: (f"{LEFT}_", f"{RIGHT}_", 2), 2: (f"{RIGHT}_", f"{LEFT}_", 1)}
        self.search, self.replace, self.side_id_other = side_map.get(self.side_id)

        # Determine the mirror plane
        plane_map = {"XY": (True, False, False), "XZ": (False, True, False), "YZ": (False, False, True)}
        self.planeXY, self.planeXZ, self.planeYZ = plane_map.get(self.mirror_plane)

        # check if mirrored already exist
        mirrored_name = self.name.replace(self.search, self.replace)
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
        for joint in self.joint_chain.guides:
            if not joint.side_id == self.side_id:
                cmds.setAttr(f"{joint.name}.side", self.side_id)

        # Mirror this bish
        mirrored_joint_chain = cmds.mirrorJoint(
            self.name,
            mirrorBehavior=True,
            mxy=self.planeXY,
            mxz=self.planeXY,
            myz=self.planeXY,
            searchReplace=(self.search, self.replace),
        )
        for joint in mirrored_joint_chain:
            cmds.setAttr(f"{joint}.side", self.side_id_other)

    @staticmethod
    def run_mirror_joint(guide):
        program = Tools(guide)
        program.mirror_joint()
