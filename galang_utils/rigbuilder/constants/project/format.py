"""THIS CONSTANT IS TO BE CHANGED BASED ON THE PROJECT NEEDS"""
from galang_utils.rigbuilder.constants.project.role import ProjectRole as Role
class ProjectFormat:
    def __init__(self, kinematcs, side):
        self.kinematics = kinematcs
        self.side = side

    @staticmethod
    def join_parts(*parts):
        return "_".join([p for p in parts if p]).strip("_")
    
    def name(self, name, item = None, function = None, properties=None, level=None, local=None, index=None):
        return self.join_parts(Role.PROJECT, self.kinematics, self.side, name, item, function, properties, level, index)
    
    @staticmethod
    def name_static(kinematics, side, name, item=None, level=None, local=None, index=None):
        return ProjectFormat.join_parts(Role.PROJECT, kinematics, side, name, item, level, index)
    