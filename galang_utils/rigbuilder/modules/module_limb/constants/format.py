"""THIS CONSTANT IS TO BE CHANGED BASED ON THE MODULE NEEDS"""


class LimbFormat:
    def __init__(self, project, kinematcs, side):
        self.project = project
        self.kinematics = kinematcs
        self.side = side

    @staticmethod
    def join_parts(*parts):
        return "_".join([p for p in parts if p]).strip("_")
    
    def name(self, name, item = None, function = None, properties=None, level=None, local=None, index=None):
        return self.join_parts(self.project, self.kinematics, self.side, name, item, function, properties, level, index)
    
    @staticmethod
    def name_static(project, kinematics, side, name, item=None, level=None, local=None, index=None):
        return LimbFormat.join_parts(project, kinematics, side, name, item, level, index)
    