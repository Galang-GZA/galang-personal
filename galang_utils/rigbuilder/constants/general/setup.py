from galang_utils.rigbuilder.constants.general import role as gen_role

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
    gen_role.ROOT: {"ids": [1]},
    gen_role.SPINE: {"ids": [6]},
    gen_role.LIMB: {"ids": [10, 2]},
    gen_role.HINGES: {"ids": [3, 11]},
    gen_role.FOOT: {"ids": [4]},
    gen_role.HAND: {"ids": [12]},
    gen_role.FINGER: {"ids": [13, 14, 19, 20, 21, 22]},
    gen_role.TOES: {"ids": [5]},
}


# Module Aim Axis
MODULE_AIM_AXIS = {
    gen_role.SPINE: "Y",
    gen_role.LIMB: "X",
    gen_role.FINGER: "X",
    gen_role.HAND: "X",
    gen_role.ROOT: "Y",
}
