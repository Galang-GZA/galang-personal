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

# Misc DAG
LOCATOR = "Loc"
DISTANCE = "Dis"

# Nodes
PAIRBLEND = "PB"
SCALEBLEND = "SB"
REVERSE = "REV"
PLUS_MINUS = "PM"
MULT_DIV = "MD"
CONDITION = "Cond"
BLEND = "Blend"

# Node Type
NORMAL = "Normalizer"
LEN_ORI = "ChainLenOri"
SCALER = "Scaler"
ATTR = "Attr"
ORI = "Ori"
BASE = "Base"
SOFT = "Soft"
BLEND = "Blend"
STRETCH = "Stretch"
PIN = "Pin"
SLIDE = "Slide"
LIMITER = "Limiter"
STATIC = "Static"
ACTIVE = "Active"

# Node combination
MD_Normal = f"{MULT_DIV}_{NORMAL}"
PM_LenStatic = f"{PLUS_MINUS}_{STATIC}"
PM_LenActive = f"{PLUS_MINUS}_{ACTIVE}"

PM_Soft = f"{PLUS_MINUS}_{SOFT}"
MD_Soft = f"{MULT_DIV}_{SOFT}"
MD_Soft_Scaler = f"{MULT_DIV}_{SOFT}_{SCALER}"
MD_Attr_Scaler = f"{MULT_DIV}_{ATTR}_{SCALER}"
COND_Soft = f"{CONDITION}_{SOFT}"
BLEND_Soft_Scaler = f"{BLEND}_{SOFT}_{SCALER}"

PM_Stretch = f"{PLUS_MINUS}_{STRETCH}"
MD_Stretch = f"{MULT_DIV}_{STRETCH}"
MD_Stretch_Scaler = f"{MULT_DIV}_{STRETCH}_{SCALER}"
COND_Stretch = f"{CONDITION}_{STRETCH}"
BLEND_Stretch_Scaler = f"{BLEND}_{STRETCH}_{SCALER}"

PM_Pin = f"{PLUS_MINUS}_{PIN}"
MD_Pin = f"{MULT_DIV}_{PIN}"
MD_Pin_Scaler = f"{MULT_DIV}_{PIN}_{SCALER}"
COND_Pin = f"{CONDITION}_{PIN}"
BLEND_Pin_Scaler = f"{BLEND}_{PIN}_{SCALER}"

PM_Slide = f"{PLUS_MINUS}_{SLIDE}"
MD_Slide = f"{MULT_DIV}_{SLIDE}"
MD_Slide_Scaler = f"{MULT_DIV}_{SLIDE}_{SCALER}"
MD_Slide_Limiter = f"{MULT_DIV}_{SLIDE}_{LIMITER}"
COND_Slide = f"{CONDITION}_{SLIDE}"
BLEND_Slide_Scaler = f"{BLEND}_{SLIDE}_{SCALER}"

LOCATOR_ORI = f"{LOCATOR}_{ORI}"
DISTANCE_ORI = f"{DISTANCE}_{ORI}"
LOCATOR_CTRL = f"{LOCATOR}_{CTRL}"
DISTANCE_CTRL = f"{DISTANCE}_{CTRL}"
LOCATOR_BASE = f"{LOCATOR}_{BASE}"
DISTANCE_BASE = f"{DISTANCE}_{BASE}"
LOCATOR_SOFT = f"{LOCATOR}_{SOFT}"
DISTANCE_SOFT = f"{DISTANCE}_{SOFT}"
LOCATOR_BLEND = f"{LOCATOR}_{BLEND}"
DISTANCE_BLEND = f"{DISTANCE}_{BLEND}"
DISTANCE_STRETCH = f"{DISTANCE}_{STRETCH}"

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
