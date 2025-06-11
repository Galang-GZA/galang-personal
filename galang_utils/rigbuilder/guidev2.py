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
        self.aim_axis: str = None
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

        if END_GUIDE or END in self.name:
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


class GuideList:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.guides: List[GuideInfo] = []
        self.guides_pv: List[GuideInfo] = []
        self.next_guides: List[str] = []
        self.get_guides(guide)

    def get_guides(self, guide):
        def recursive_get_guide(guide: GuideInfo):
            if not guide.is_guide:
                return

            if PV in guide.name:
                self.guides_pv.append(guide)
            else:
                self.guides.append(guide)

            children = cmds.listRelatives(guide.name, c=True, typ="joint")
            if not children:
                return
            for child in children:
                child_guide = GuideInfo(child)
                if child_guide.is_module:
                    self.next_guides.append(child)
                elif child_guide.is_guide_end:
                    continue
                else:
                    recursive_get_guide(child_guide)

        if not self.guide.is_guide:
            return

        recursive_get_guide(self.guide)

    # Debugging procedures
    def __repr__(self):
        guides = [guide.name for guide in self.guides]
        guides_pv = [guide.name for guide in self.guides_pv]
        return (
            f"<module = {self.guide.name}, "
            f"guides = {guides}, "
            f"guides_pv = {guides_pv}>, "
            f"next modules = {self.next_guides}"
        )


class ModuleData:
    def __init__(self, guide):
        self.module_map: Dict = {}
        self.get_data(guide)

    def get_data(self, guide: str) -> None:
        def recursive_get_data(guide):
            # Determine module type
            module_typ = None
            module_id = cmds.getAttr(f"{guide}.type")
            for module_name, data in MODULE_MAP.items():
                if module_id in data["ids"]:
                    module_typ = module_name
                    break
            if module_typ is None:
                return

            # Determine module aim axis
            aim_axis = MODULE_AIM_AXIS.get(module_typ)

            # Map the guide module with contents
            contents = GuideList(guide)
            self.module_map[str(guide)] = {
                TYPE: module_typ,
                CONTENTS: contents,
                AXIS: aim_axis,
            }

            # Recursive get modules for the next guides
            if contents.next_guides:
                for next_guide in contents.next_guides:
                    recursive_get_data(next_guide)

        recursive_get_data(guide)

    # Debugging procedures
    def __repr__(self):
        lines = ["<ModuleData>"]
        for guide_name, data in self.module_map.items():
            module_typ = data[TYPE]
            aim_axis = data[AXIS]
            guide_list = data[CONTENTS]

            lines.append(f"    Module       : {guide_name} (type = {module_typ}, axis = {aim_axis})")
            lines.append(f"    Guides       : {[g.name for g in guide_list.guides]}")
            lines.append(f"    Guides PV    : {[g.name for g in guide_list.guides_pv]}")
            lines.append(f"    Next Modules : {guide_list.next_guides}")
            lines.append("")

        return "\n".join(lines)
