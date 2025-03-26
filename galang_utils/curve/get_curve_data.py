"""
GET ALL CURVE DATA IN CUSTOM CONTROL GROUP
"""

import maya.cmds as cmds


def printCurveData():
    # Dictionary to store curve data
    Curves_Data = {}

    # List all custom control to be stored
    CustomControl = cmds.ls(sl=True)[0]

    Shape = cmds.listRelatives(CustomControl, shapes=True, type="nurbsCurve")[0]

    # Get curves properties
    Degree = cmds.getAttr(f"{Shape}.degree")
    Control_Points = cmds.getAttr(f"{Shape}.cv[*]")  # List of CV positions
    Knots = cmds.getAttr(f"{Shape}.knots") if cmds.attributeQuery("knots", node=Shape, exists=True) else []

    # Storing the data
    Curves_Data[CustomControl] = {"Degree": Degree, "Control_Points": Control_Points, "Knots": Knots}

    print(Curves_Data)
