"""IT IS EXTREMELY IMPORTANT FOR THE JOINTS TO BE TYPED"""

from maya import cmds
from typing import List, Dict
from galang_utils.rigbuilder.guide import *
from galang_utils.rigbuilder.constants import *


class JointReorient:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.input = GuideList(guide)

    def program(self):
        joint_to_reorient = [guide for guide in self.input.guides if guide.module_start]
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
        run = JointReorient(root_joint)
        run.program()
