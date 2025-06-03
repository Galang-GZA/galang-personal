"""THIS CONSTANT IS TO BE CHANGED BASED ON THE MODULE NEEDS"""


# Name Format
def hand_join_parts(*parts):
    return "_".join([p for p in parts if p]).strip("_")


def hand_level_format(PJ, kinematics, side, name, level, item=None, local=None):
    return hand_join_parts(PJ, kinematics, side, name, item, level)


def hand_joint_format(PJ, kinematics, side, name, JNT, local=None):
    return hand_join_parts(PJ, kinematics, side, name, JNT)


def hand_control_format(PJ, kinematics, side, name, CTRL, local=None):
    return hand_join_parts(PJ, kinematics, side, name, CTRL)


def hand_misc_format(PJ, kinematics, side, name, MISC, local=None):
    return hand_join_parts(PJ, kinematics, side, name, MISC)
