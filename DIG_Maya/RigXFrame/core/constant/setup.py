from RigXFrame.core.constant import role as xframe_role

# Side
DEFAULT_LEFT = "lt"
DEFAULT_RIGHT = "rt"
DEFAULT_CENTER = None

MIRROR_AXIS_DATA = {
    "X": {"orientation": [0, 180, 0], "scale": [1, -1, 1], "scale_child": [-1, 1, 1]},
    "Y": {"orientation": [180, 0, 0], "scale": [-1, 1, 1], "scale_child": [1, -1, 1]},
    "Z": {"orientation": [0, 0, 180], "scale": [1, 1, -1], "scale_child": [1, 1, -1]},
}

MODULE_MAP = {
    xframe_role.ROOT: {"ids": [1]},
    xframe_role.SPINE: {"ids": [6]},
    xframe_role.LIMB: {"ids": [10, 2]},
    xframe_role.HINGES: {"ids": [3, 11]},
    xframe_role.FOOT: {"ids": [4]},
    xframe_role.HAND: {"ids": [12]},
    xframe_role.FINGER: {"ids": [13, 14, 19, 20, 21, 22]},
    xframe_role.TOES: {"ids": [5]},
}


# Module Aim Axis
MODULE_AIM_AXIS = {
    xframe_role.SPINE: "Y",
    xframe_role.LIMB: "X",
    xframe_role.FINGER: "X",
    xframe_role.HAND: "X",
    xframe_role.ROOT: "Y",
}
