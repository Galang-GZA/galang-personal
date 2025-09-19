from typing import Dict
from galang_utils.rig_x_frame.constants.project import role as role
from galang_utils.rig_x_frame.constants.general import role as gen_role


# Node Flags
NODE_LEVEL_FLAGS = {
    role.MAIN: {
        role.OFFSET: False,
        role.SDK: False,
        role.LINK: False,
        role.CONSTRAINT: True,
        role.MIRROR: True,
        role.GROUP: True,
    },
    role.SUB: {
        role.OFFSET: False,
        role.SDK: False,
        role.LINK: False,
        role.CONSTRAINT: False,
        role.MIRROR: False,
        role.GROUP: True,
    },
}
