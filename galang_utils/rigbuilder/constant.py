# Project
PJ = None  # Project Code
JNT = "jnt"  # Joint
NUM = "001"  # Numbers
IK = "ik"  # Inverse Kinematics
FK = "fk"  # Forward Kinematics
RESULT = "result"  # Result of IK & FK
BIND = "Bind"  # Bind Joint
CTRL = "ctrl"  # Controller


# Node Levels
GROUP = "grp"
OFFSET = "offset"
SDK = "sdk"
LINK = "link"
MIRROR = "mirror"

NODE_LEVELS = [OFFSET, SDK, LINK, MIRROR, GROUP]
NODE_DEFAULT_FLAGS = {OFFSET: True, SDK: True, LINK: True, MIRROR: True, GROUP: True}

# Side
DEFAULT_LEFT = "L"
DEFAULT_RIGHT = "R"
DEFAULT_CENTER = ""

LEFT = "lt"
RIGHT = "rt"
CENTER = None

SIDE_MAP = {0: CENTER, 1: LEFT, 2: RIGHT}

# Mirror Side
MIRROR_SIDE_ID = 2
MIRROR_AXIS = "X"
MIRROR_AXIS_DATA = {
    "X": {"orientation": [0, 180, 0], "scale": [1, -1, 1], "scale_child": [-1, 1, 1]},
    "Y": {"orientation": [180, 0, 0], "scale": [-1, 1, 1], "scale_child": [1, -1, 1]},
    "Z": {"orientation": [0, 0, 180], "scale": [1, 1, -1], "scale_child": [1, 1, -1]},
}

# Joint Mirror
MIRROR_PLANE = "YZ"

# Color Library
COLOR_INDEX = {"red": 13, "blue": 6, "yellow": 17, "green": 14, "cyan": 18, "magenta": 9, "black": 1, "white": 16}

MAIN_COLOR = {1: COLOR_INDEX["blue"], 2: COLOR_INDEX["red"], 0: COLOR_INDEX["yellow"]}
BENDY_COLOR = {1: COLOR_INDEX["cyan"], 2: COLOR_INDEX["magenta"], 0: COLOR_INDEX["green"]}


# Name Format
def _join_parts(*parts):
    return "_".join([p for p in parts if p]).strip("_")


def joint_format(kinematics, side, name):
    return _join_parts(PJ, kinematics, side, name, JNT)


def control_format(kinematics, side, name):
    return _join_parts(PJ, kinematics, side, name, CTRL)


def level_format(kinematics, side, name, level, item=None):
    return _join_parts(PJ, kinematics, side, name, item, level)


# Module name
MODULE = "Module"
ROOT = "Root"
FINGER = "Finger"
LIMB = "Limb"
HINGES = "Hinges"
SPINE = "Spine"
HAND = "Hand"
FOOT = "foot"
TOES = "toes"

MODULE_MAP = {
    ROOT: {"ids": [1], "contents": []},
    SPINE: {"ids": [6], "contents": [SPINE]},
    LIMB: {"ids": [10, 2], "contents": [LIMB, HINGES, HAND, FOOT]},
    HINGES: {"ids": [3, 11], "contents": []},
    FOOT: {"ids": [4], "contents": [FOOT, TOES]},
    HAND: {"ids": [12], "contents": [HAND]},
    FINGER: {"ids": [13, 14, 19, 20, 21, 22], "contents": [FINGER]},
    TOES: {"ids": [5], "contents": []},
}

# Module Aim Axis
MODULE_AIM_AXIS = {SPINE: "Y", LIMB: "X", FINGER: "X", HAND: "X", ROOT: "Y"}


# Nodes
PAIRBLEND = "PB"
SCALEBLEND = "SB"
REVERSE = "REV"

# Custom Attribute
IKFKSWITCH = "ikFKSwitch"
