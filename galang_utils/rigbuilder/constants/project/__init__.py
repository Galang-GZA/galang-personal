# Name Format
def _join_parts(*parts):
    return "_".join([p for p in parts if p]).strip("_")


def name_format(project, kinematics, side, name, level, item=None):
    return _join_parts(project, kinematics, side, name, item, level)
