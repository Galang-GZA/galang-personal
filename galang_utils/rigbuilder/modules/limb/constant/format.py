"""THIS CONSTANT IS TO BE CHANGED BASED ON THE MODULE NEEDS"""
from galang_utils.rigbuilder.constant.project import role as TASK_ROLE


class LimbFormat:
    def __init__(self, side, kinematcs=None):
        self.kinematics = kinematcs
        self.side = side

    @staticmethod
    def join_parts(*parts):
        return "_".join([p for p in parts if p]).strip("_")
    
    def name(self, name, type = None, properties1=None, properties2=None, level=None, local=None, index=None):
        return self.join_parts(TASK_ROLE.PROJECT, self.kinematics, self.side, name, type, properties1, properties2, level, index)
    
    @staticmethod
    def name_static(name, side, kinematics=None, type=None, properties1=None, properties2=None, level=None, local=None, index=None):
        return LimbFormat.join_parts(TASK_ROLE.PROJECT, kinematics, side, name, type, properties1, properties2, level, index)
    