"""THIS CONSTANT IS TO BE CHANGED BASED ON THE PROJECT NEEDS"""

from typing import List, Dict

# Project
PJ = None  # Project Code
JNT = "jnt"  # Joint
NUM = "001"  # Numbers
IK = "ik"  # Inverse Kinematics
FK = "fk"  # Forward Kinematics
NK = None  # None Kinematics
RESULT = "result"  # Result of IK & FK
BIND = "Bind"  # Bind Joint
CTRL = "ctrl"  # Controller
MISC = "misc"  # Miscellaneous
PV = "pv"  # Pole Vector

# Node Levels
GROUP = "grp"
OFFSET = "offset"
SDK = "sdk"
LINK = "link"
MIRROR = "mirror"
LOCAL = "local"

NODE_MAIN_LEVELS = [OFFSET, SDK, LINK, MIRROR, GROUP]
NODE_LOCAL_LEVELS = [MIRROR, GROUP]
NODE_DEFAULT_FLAGS = {OFFSET: True, SDK: True, LINK: True, MIRROR: True, GROUP: True}

# Side
DEFAULT_LEFT = "lt"
DEFAULT_RIGHT = "rt"
DEFAULT_CENTER = None

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
COLOR_INDEX = {
    "red": 13,
    "blue": 6,
    "yellow": 17,
    "green": 14,
    "cyan": 18,
    "magenta": 9,
    "black": 1,
    "white": 16,
}

MAIN_COLOR = {1: COLOR_INDEX["blue"], 2: COLOR_INDEX["red"], 0: COLOR_INDEX["yellow"]}
BENDY_COLOR = {1: COLOR_INDEX["cyan"], 2: COLOR_INDEX["magenta"], 0: COLOR_INDEX["green"]}


# Name Format
def _join_parts(*parts):
    return "_".join([p for p in parts if p]).strip("_")


def name_format(kinematics, side, name, level, item=None):
    return _join_parts(PJ, kinematics, side, name, item, level)
