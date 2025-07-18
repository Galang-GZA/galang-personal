"""THIS CONSTANT IS TO BE CHANGED BASED ON THE MODULE NEEDS"""


# Name Format
def finger_join_parts(*parts):
    return "_".join([p for p in parts if p]).strip("_")


def finger_level_format(PJ, kinematics, side, name, level, item=None, local=None):
    return finger_join_parts(PJ, kinematics, side, name, item, level)


def finger_joint_format(PJ, kinematics, side, name, JNT, local=None):
    return finger_join_parts(PJ, kinematics, side, name, JNT)


def finger_control_format(PJ, kinematics, side, name, CTRL, local=None):
    return finger_join_parts(PJ, kinematics, side, name, CTRL)


def finger_misc_format(PJ, kinematics, side, name, MISC, local=None):
    return finger_join_parts(PJ, kinematics, side, name, MISC)
