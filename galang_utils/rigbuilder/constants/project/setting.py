from galang_utils.rigbuilder.constants.project.role import ProjectRole as Role

class ProjectSetting:
    def __init__(self):
        # Side Mapping
        self.SIDE_MAP = {0: Role.CENTER, 1: Role.LEFT, 2: Role.RIGHT}

        # Mirror Side
        self.MIRROR_SIDE_ID = 2
        self.MIRROR_AXIS = "X"

        # Joint Mirror
        self.MIRROR_PLANE = "YZ"

        # Node Levels
        self.NODE_MAIN_LEVELS = [Role.OFFSET, Role.SDK, Role.LINK, Role.MIRROR, Role.GROUP]
        self.NODE_SUB_LEVELS = [Role.LINK, Role.MIRROR, Role.GROUP]
        self.NODE_DEFAULT_FLAGS = {Role.OFFSET: True, Role.SDK: True, Role.LINK: True, Role.MIRROR: True, Role.GROUP: True}

        # Color Library
        self.COLOR_INDEX = {"red": 13, "blue": 6, "yellow": 17, "green": 14, "cyan": 18, "magenta": 9, "black": 1, "white": 16}

        self.MAIN_COLOR = {1: self.COLOR_INDEX["blue"], 2: self.COLOR_INDEX["red"], 0: self.COLOR_INDEX["yellow"]}
        self.SUB_COLOR = {1: self.COLOR_INDEX["cyan"], 2: self.COLOR_INDEX["magenta"], 0: self.COLOR_INDEX["green"]}

        # Ammounts
        self.LEN_DETAILS = 3

