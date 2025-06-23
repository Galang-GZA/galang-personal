from maya import cmds
from typing import List, Dict
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *


class GuideInfo:
    def __init__(self, joint_name: str):
        self.name: str = joint_name
        self.name_raw: str = None
        self.is_guide: bool = False
        self.is_guide_end: bool = False
        self.is_module: bool = False
        self.side_id: int = None
        self.side: str = None
        self.parent: str = None
        self.parent_raw: str = None
        self.position: List[float] = None
        self.orientation: List[float] = None
        self.scale: List[float] = None
        self.size: int = None
        self.__init__joint()

    @staticmethod
    def safe_get_attr(attr, default=None):
        try:
            return cmds.getAttr(attr)
        except Exception:
            return default

    # Innitialize guide joint to get infos
    def __init__joint(self):
        # Defining the guide properties
        if not cmds.objectType(self.name, i="joint"):
            cmds.warning(f"{self.name} not a joint this is")
            return
        self.is_guide = True

        if END_GUIDE in self.name:
            self.is_guide_end = True

        if self.safe_get_attr(f"{self.name}.drawLabel") == 1:
            self.is_module = True

        # Defining guide's parent
        parent = cmds.listRelatives(self.name, p=True, typ="joint")
        if parent:
            self.parent = parent[0]

        # Defining guide's side and raw name
        self.side_id = self.safe_get_attr(f"{self.name}.side")
        self.side = SIDE_MAP.get(self.side_id)
        if self.side:
            self.name_raw = self.name.replace(f"{self.side}_", "")
            self.parent_raw = self.parent.replace(f"{self.side}_", "")
        else:
            self.name_raw = self.name
            self.parent_raw = self.parent

        # Querying guide's translation
        self.position = cmds.xform(self.name, q=True, t=True, ws=True)
        self.orientation = cmds.xform(self.name, q=True, ro=True, ws=True)
        self.scale = cmds.xform(self.name, q=True, s=True, ws=True)
        self.size = cmds.getAttr(f"{self.name}.radius")

    # Debugging procedures
    def __repr__(self):
        return (
            f"<GuideInfo name = '{self.name}', side = '{self.side}', "
            f"is module = {self.is_module}, parent = '{self.parent}', "
            f"position = {self.position}, orientation = {self.orientation}, size = {self.size}>"
        )

    # I literally have no idea how to read this one, just copied from uncle GPT
    def __str__(self):
        side = self.side or "?"
        pos = f"({', '.join(f'{p:.2f}' for p in self.position)})" if self.position else "unknown"
        orient = f"({', '.join(f'{o:.2f}' for o in self.orientation)})" if self.orientation else "unknown"
        return f"[{side}] {self.name} at {pos}, orientation = {orient}, size is {self.size}, module = {self.is_module}"


class ModuleInfo:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.type: str = None
        self.axis: str = None
        self.guides: List[GuideInfo] = []
        self.guides_end: List[GuideInfo] = []
        self.guides_pv: List[GuideInfo] = []
        self.child: List = []
        self.parent: str = None
        self.__init__module(guide)

    def __init__module(self, guide):
        def recursive_get_parent_module(guide: GuideInfo):
            if not guide.is_guide:
                return
            parent_list = cmds.listRelatives(guide.name, p=True, typ="joint")
            if parent_list:
                parent = GuideInfo(parent_list[0])
                if parent.is_module:
                    self.parent = parent.name
                else:
                    recursive_get_parent_module(parent)

        def recursive_get_guide(guide: GuideInfo):
            if not guide.is_guide:
                return
            # Determine module type
            if guide.is_module:
                module_id = cmds.getAttr(f"{guide.name}.type")
                for module_name, data in MODULE_MAP.items():
                    if module_id in data["ids"]:
                        self.type = module_name
                        break
                # Determine module aim axis
                self.axis = MODULE_AIM_AXIS.get(self.type)

            if PV in guide.name:
                self.guides_pv.append(guide)
            else:
                self.guides.append(guide)

            children = cmds.listRelatives(guide.name, c=True, typ="joint")
            if not children:
                return
            else:
                children_guide = [g for g in children if PV not in g]
                for child in children:
                    child_guide = GuideInfo(child)
                    if child_guide.is_module:
                        if len(children_guide) == 1:
                            self.guides_end.append(child_guide)
                        self.child.append(child)
                    elif child_guide.is_guide_end:
                        continue
                    else:
                        recursive_get_guide(child_guide)

        if not self.guide.is_guide:
            return

        recursive_get_guide(self.guide)
        recursive_get_parent_module(self.guide)

    # Debugging procedures
    def __repr__(self):
        lines = [f"<Module Info for module = {self.guide.name}, type = {self.type}, axis = {self.axis}>"]
        lines.append(f"    Guides        : {[g.name for g in self.guides]}")
        lines.append(f"    Guides End    : {[g.name for g in self.guides_end]}")
        lines.append(f"    Guides PV     : {[g.name for g in self.guides_pv]}")
        lines.append(f"    Parent Module : {self.parent}")
        lines.append(f"    Child Modules : {self.child}")
        return "\n".join(lines)
