from maya import cmds
from typing import List, Dict
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.modules.module_hand.constant import *


class Hand_GuideInfo:
    def __init__(self, joint_name):
        self.name = joint_name
        self.name_raw = None
        self.is_guide = False
        self.is_guide_end = False
        self.is_guide_misc = False
        self.aim_axis = None
        self.module_id = 0
        self.module_start = False
        self.module = None
        self.side_id = 0
        self.side = None
        self.parent = None
        self.parent_raw = None
        self.children = None
        self.position = None
        self.orientation = None
        self.scale = None
        self.size = None
        self.__init__joint()

    def __init__joint(self):
        if not cmds.objectType(self.name, i="joint"):
            cmds.warning(f"{self.name} not a joint this is")
            return
        self.is_guide = True
        if cmds.getAttr(f"{self.name}.drawStyle") == 2:
            self.is_guide_end = True
        if cmds.getAttr(f"{self.name}.drawStyle") == 3:
            self.is_guide_misc = True

        self.module_id = cmds.getAttr(f"{self.name}.type")
        if self.module_id == 18:
            self.module = cmds.getAttr(f"{self.name}.otherType")
        else:
            for module_name, data in MODULE_MAP.items():
                if self.module_id in data["ids"]:
                    self.module = module_name
        self.aim_axis = MODULE_AIM_AXIS.get(self.module)
        if not self.aim_axis:
            self.aim_axis = "X"

        parent = cmds.listRelatives(self.name, p=True, typ="joint")
        if parent:
            self.parent = parent[0]
        self.children = cmds.listRelatives(self.name, c=True, typ="joint")

        self.side_id = cmds.getAttr(f"{self.name}.side")
        self.side = SIDE_MAP.get(self.side_id)
        if self.side:
            self.name_raw = self.name.replace(f"{self.side}_", "")
            self.parent_raw = self.parent.replace(f"{self.side}_", "")
        else:
            self.name_raw = self.name
            self.parent_raw = self.parent

        if cmds.getAttr(f"{self.name}.drawLabel") == 1:
            self.module_start = True

        self.position = cmds.xform(self.name, q=True, t=True, ws=True)
        self.orientation = cmds.xform(self.name, q=True, ro=True, ws=True)
        self.scale = cmds.xform(self.name, q=True, s=True, ws=True)
        self.size = cmds.getAttr(f"{self.name}.radius")


class Hand_GuideList:
    def __init__(self, guide=None):
        self.guide = Hand_GuideInfo(guide)
        self.guides: List[Hand_GuideInfo] = []
        if guide:
            self.get_guides(guide)

    def get_guides(self, guide_joint):
        guides_all: List = []

        def recursive_get_guide(guide_joint, guides_all: List):
            guide_joint = Hand_GuideInfo(guide_joint)
            if not guide_joint.is_guide:
                return

            if not self.guide.module == ROOT:
                module_contents: Dict = MODULE_MAP.get(self.guide.module, {}).get("contents", [])
                if guide_joint.module not in module_contents:
                    return

            guides_all.append(guide_joint)
            children = cmds.listRelatives(guide_joint.name, c=True, typ="joint")
            if not children:
                return
            for child in children:
                recursive_get_guide(child, guides_all)

        first_guide = Hand_GuideInfo(guide_joint)
        if not first_guide.is_guide:
            return

        recursive_get_guide(guide_joint, guides_all)
        self.guides = guides_all
