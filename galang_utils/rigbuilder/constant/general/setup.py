from galang_utils.rigbuilder.constant.general import role as general_role

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
    general_role.ROOT: {"ids": [1]},
    general_role.SPINE: {"ids": [6]},
    general_role.LIMB: {"ids": [10, 2]},
    general_role.HINGES: {"ids": [3, 11]},
    general_role.FOOT: {"ids": [4]},
    general_role.HAND: {"ids": [12]},
    general_role.FINGER: {"ids": [13, 14, 19, 20, 21, 22]},
    general_role.TOES: {"ids": [5]},
}


# Module Aim Axis
MODULE_AIM_AXIS = {
    general_role.SPINE: "Y",
    general_role.LIMB: "X",
    general_role.FINGER: "X",
    general_role.HAND: "X",
    general_role.ROOT: "Y",
}
