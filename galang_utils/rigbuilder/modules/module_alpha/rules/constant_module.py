"""THIS CONSTANT IS TO BE CHANGED BASED ON THE MODULE NEEDS"""


# Name Format
def limb_join_parts(*parts):
    return "_".join([p for p in parts if p]).strip("_")


def limb_level_format(PJ, kinematics, side, name, level, item=None, local=None):
    return limb_join_parts(PJ, kinematics, side, name, item, level)


def limb_joint_format(PJ, kinematics, side, name, JNT, local=None):
    return limb_join_parts(PJ, kinematics, side, name, JNT)


def limb_control_format(PJ, kinematics, side, name, CTRL, local=None):
    return limb_join_parts(PJ, kinematics, side, name, CTRL)


def limb_misc_format(PJ, kinematics, side, name, MISC, local=None):
    return limb_join_parts(PJ, kinematics, side, name, MISC)
