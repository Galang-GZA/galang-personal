"""Create Hand Rig Based On the Guide Joints"""

from maya import cmds
from galang_utils.rig_x_frame.constants import *
from galang_utils.rig_x_frame.guide import GuideInfo, GuideList
from galang_utils.rig_x_frame.controls import ControlCreator


class ModuleAssembly:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.input = GuideList(guide)
        self.builder_map = {LIMB: ModuleLimb, FINGER: ModuleFinger}

    def build(self):
        for g in self.input.guides:
            if g.module_start:
                builder_class = self.builder_map.get(g.module)
                if not builder_class:
                    print(f"{g.name} has no module, skipppz for now")
                    continue
                # print(g.name)
                builder_instance = builder_class(g.name)
                builder_instance.build()

    def assembly(self):
        pass
