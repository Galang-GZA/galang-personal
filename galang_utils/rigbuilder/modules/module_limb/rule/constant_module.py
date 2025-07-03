"""THIS CONSTANT IS TO BE CHANGED BASED ON THE MODULE NEEDS"""


# Name Format
def limb_join_parts(*parts):
    return "_".join([p for p in parts if p]).strip("_")


def limb_level_format(PJ, kinematics, side, name, level, item=None, local=None, index=None):
    return limb_join_parts(PJ, kinematics, side, name, item, level, index)


def limb_format(PJ, kinematics, side, name, item=None, local=None, index=None):
    return limb_join_parts(PJ, kinematics, side, name, item, local, index)


def limb_joint_format(PJ, kinematics, side, name, JNT, local=None, index=None):
    return limb_join_parts(PJ, kinematics, side, name, JNT, index)


def limb_control_format(PJ, kinematics, side, name, CTRL, local=None, index=None):
    return limb_join_parts(PJ, kinematics, side, name, CTRL, index)


def limb_node_format(PJ, kinematics, side, name, node, index=None):
    return limb_join_parts(PJ, kinematics, side, name, node, index)
