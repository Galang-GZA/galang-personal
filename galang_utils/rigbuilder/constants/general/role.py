# Module
MODULE = "module"
ROOT = "root"
FINGER = "Finger"
LIMB = "limb"
HINGES = "hinges"
SPINE = "spine"
HAND = "hand"
FOOT = "foot"
TOES = "toes"
CARPAL = "MetaCarpal"
END_GUIDE = "EndGuide"
END = "End"

MODULE_MAP = {
    ROOT: {"ids": [1]},
    SPINE: {"ids": [6]},
    LIMB: {"ids": [10, 2]},
    HINGES: {"ids": [3, 11]},
    FOOT: {"ids": [4]},
    HAND: {"ids": [12]},
    FINGER: {"ids": [13, 14, 19, 20, 21, 22]},
    TOES: {"ids": [5]},
}

# Module Misc
TYPE = "typ"
AXIS = "aim_axis"
PARENT = "parent_module"
DATA = "data"
PROPERTIES = "properties"
SETTINGS = "setings"

# Module Aim Axis
MODULE_AIM_AXIS = {SPINE: "Y", LIMB: "X", FINGER: "X", HAND: "X", ROOT: "Y"}

# Class
COMPONENT = "component"
OPERATOR = "operator"
