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
    ROOT: {"ids": [1], "contents": []},
    SPINE: {"ids": [6], "contents": [SPINE]},
    LIMB: {"ids": [10, 2], "contents": [LIMB, HINGES, HAND, FOOT]},
    HINGES: {"ids": [3, 11], "contents": []},
    FOOT: {"ids": [4], "contents": [FOOT, TOES]},
    HAND: {"ids": [12], "contents": [HAND, CARPAL]},
    FINGER: {"ids": [13, 14, 19, 20, 21, 22], "contents": [FINGER]},
    TOES: {"ids": [5], "contents": []},
}

# Module Misc
TYPE = "typ"
CONTENTS = "contents"
AXIS = "aim_axis"
PARENT = "parent_module"
DATA = "data"
PROPERTIES = "properties"
SETTINGS = "setings"


# Module Aim Axis
MODULE_AIM_AXIS = {SPINE: "Y", LIMB: "X", FINGER: "X", HAND: "X", ROOT: "Y"}


# Nodes
PAIRBLEND = "PB"
SCALEBLEND = "SB"
REVERSE = "REV"

# Custom Attribute
IKFKSWITCH = "ikFKSwitch"
