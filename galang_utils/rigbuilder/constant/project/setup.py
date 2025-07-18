from galang_utils.rigbuilder.constant.project import role as Role


# Side Mapping
SIDE_MAP = {0: Role.CENTER, 1: Role.LEFT, 2: Role.RIGHT}

# Mirror Side
MIRROR_SIDE_ID = 2
MIRROR_AXIS = "X"

# Joint Mirror
MIRROR_PLANE = "YZ"

# Node Levels
NODE_MAIN_LEVELS = [Role.OFFSET, Role.SDK, Role.LINK, Role.MIRROR, Role.GROUP]
NODE_SUB_LEVELS = [Role.LINK, Role.MIRROR, Role.GROUP]
NODE_DEFAULT_FLAGS = {Role.OFFSET: True, Role.SDK: True, Role.LINK: True, Role.MIRROR: True, Role.GROUP: True}

# Color Library
COLOR_INDEX = {"red": 13, "blue": 6, "yellow": 17, "green": 14, "cyan": 18, "magenta": 9, "black": 1, "white": 16}

MAIN_COLOR = {1: COLOR_INDEX["blue"], 2: COLOR_INDEX["red"], 0: COLOR_INDEX["yellow"]}
SUB_COLOR = {1: COLOR_INDEX["cyan"], 2: COLOR_INDEX["magenta"], 0: COLOR_INDEX["green"]}

# Ammounts
LEN_DETAILS = 3

