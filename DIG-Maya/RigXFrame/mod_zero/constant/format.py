"""THIS CONSTANT IS TO BE CHANGED BASED ON THE PROJECT NEEDS"""

from galang_utils.rig_x_frame.constants.project import role


class ProjectFormat:
    def __init__(self, kinematcs, side):
        self.kinematics = kinematcs
        self.side = side

    @staticmethod
    def join_parts(*parts):
        return "_".join([p for p in parts if p]).strip("_")

    def name(self, name, item=None, function=None, properties=None, level=None, local=None, index=None):
        return self.join_parts(
            role.PROJECT, self.kinematics, self.side, name, item, function, properties, level, index
        )

    @staticmethod
    def name_static(kinematics, side, name, item=None, level=None, local=None, index=None):
        return ProjectFormat.join_parts(role.PROJECT, kinematics, side, name, item, level, index)
