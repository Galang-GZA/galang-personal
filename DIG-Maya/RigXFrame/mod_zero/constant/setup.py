from typing import Dict
from galang_utils.rig_x_frame.constants.project import role as role
from galang_utils.rig_x_frame.constants.general import role as gen_role

# Side Mapping
SIDE_MAP = {0: role.CENTER, 1: role.LEFT, 2: role.RIGHT}

# Mirror Side
MIRROR_SIDE_ID = 2
MIRROR_AXIS = "X"
MIRROR_SCALE = True

# Joint Mirror
MIRROR_PLANE = "YZ"


# Node Levels
NODE_MAIN_LEVELS = [role.OFFSET, role.SDK, role.LINK, role.CONSTRAINT, role.MIRROR, role.GROUP]
NODE_SUB_LEVELS = [role.OFFSET, role.SDK, role.LINK]

# Color Library
COLOR_INDEX = {"red": 13, "blue": 6, "yellow": 17, "green": 14, "cyan": 18, "magenta": 9, "black": 1, "white": 16}

MAIN_COLOR: Dict = {1: COLOR_INDEX["blue"], 2: COLOR_INDEX["red"], 0: COLOR_INDEX["yellow"]}
SUB_COLOR: Dict = {1: COLOR_INDEX["cyan"], 2: COLOR_INDEX["magenta"], 0: COLOR_INDEX["green"]}

# Control type mapping
MAIN = {gen_role.LEVEL: MAIN_COLOR, gen_role.COLOR: MAIN_COLOR}
SUB = {gen_role.LEVEL: SUB_COLOR, gen_role.COLOR: SUB_COLOR}

# Ammounts
SUB_DIVS = 3

# Placeholder
INDEX = "A PLACEHOLDER TO BE REPLACED BY DESIRED INTEGER"
