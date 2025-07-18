
from galang_utils.rigbuilder.constant.general import role as GEN_ROLE

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
    GEN_ROLE.ROOT: {"ids": [1]},
    GEN_ROLE.SPINE: {"ids": [6]},
    GEN_ROLE.LIMB: {"ids": [10, 2]},
    GEN_ROLE.HINGES: {"ids": [3, 11]},
    GEN_ROLE.FOOT: {"ids": [4]},
    GEN_ROLE.HAND: {"ids": [12]},
    GEN_ROLE.FINGER: {"ids": [13, 14, 19, 20, 21, 22]},
    GEN_ROLE.TOES: {"ids": [5]},
}



# Module Aim Axis
MODULE_AIM_AXIS = {GEN_ROLE.SPINE: "Y", GEN_ROLE.LIMB: "X", GEN_ROLE.FINGER: "X", GEN_ROLE.HAND: "X", GEN_ROLE.ROOT: "Y"}