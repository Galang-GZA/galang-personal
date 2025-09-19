from maya import cmds
from typing import List
from galang_utils.rig_x_frame.constants.project import role as role
from rig_x_frame.mod_zero.base.component.dag import Node
from galang_utils.rig_x_frame.core.guide import ModuleInfo
from galang_utils.rig_x_frame.mod_zero.base.component.dag import Node
from galang_utils.rig_x_frame.mod_zero.base.component.control import ControlSet
from core.component.joint import JointSet


class FKComponent:
    def __init__(self, module: ModuleInfo):
        side = module.side
        guide = module.guide
        guides = module.guides
        guide_names = (g.name for g in guides)
        positions = (g.position for g in guides)
        orientations = (g.orientation for g in guides)

        # Pre compute dag components
        self.group = Node(guide.name, side, [role.FK, role.RIG, role.GROUP], positions, orientations)
        self.joints = JointSet(guide_names, side, [role.FK], positions, orientations)
        self.controls = ControlSet(guide_names, side, [role.FK], positions, orientations)

    def create(self):
        self.__create_fk_components()
        self.__parent_fk_components()

    def __create_fk_components(self):
        # STEP 0 : CREATE PRE COMPUTED COMPONENTS
        components: List[Node] = [self.group, self.joints, self.controls]
        for component in components:
            component.create()

    def __parent_fk_components(self):
        # STEP 0 : PARENT PRE COMPUTED COMPONENTS
        components: List[Node] = [self.joints, self.controls]
        for component in components:
            cmds.parent(component, self.group)
