from typing import List
from maya import cmds

from galang_utils.rigbuilder.constants.project import role as role
from galang_utils.rigbuilder.cores.guide import ModuleInfo
from galang_utils.rigbuilder.modules.base.component.dag import Node


class GroupComponent:
    def __init__(self, module: ModuleInfo):
        guide = module.guide
        position = guide.position
        orientation = guide.orientation

        # Pre compute dag components
        self.rig = Node(guide.name, module.side, [role.RIG, role.GROUP], position, orientation)
        self.dnt = Node(guide.name, module.side, [role.DNT, role.GROUP], position, orientation)
        self.constraint = Node(guide.name, module.side, [role.CONSTRAINT, role.BUFFER], position, orientation)

    def create(self):
        self.__create_group_components()
        self.__parent_group_components()

    def __create_group_components(self):
        # STEP 0 : CREATE PRE COMPUTED COMPONENTS
        groups: List[Node] = [self.rig, self.dnt, self.constraint]
        for group in groups:
            group.create()

    def __parent_group_components(self):
        # STEP 0 : PARENT CONSTRAINT BUFFER TO DNT
        cmds.parent(self.constraint, self.dnt)
