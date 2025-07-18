"""THIS CONSTANT IS TO BE CHANGED BASED ON THE MODULE NEEDS"""


# Name Format
def base_join_parts(*parts):
    return "_".join([p for p in parts if p]).strip("_")


def base_level_format(PJ, kinematics, side, name, level, item=None, local=None):
    return base_join_parts(PJ, kinematics, side, name, item, level)


def base_joint_format(PJ, kinematics, side, name, JNT, local=None):
    return base_join_parts(PJ, kinematics, side, name, JNT)


def base_control_format(PJ, kinematics, side, name, CTRL, local=None):
    return base_join_parts(PJ, kinematics, side, name, CTRL)


def base_misc_format(PJ, kinematics, side, name, MISC, local=None):
    return base_join_parts(PJ, kinematics, side, name, MISC)
