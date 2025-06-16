from maya import cmds
from typing import List, Dict, Union
from galang_utils.curve.shapes_library import *
from galang_utils.rigbuilder.constants.constant_general import *
from galang_utils.rigbuilder.constants.constant_project import *
from galang_utils.rigbuilder.guides.guide import GuideInfo, ModuleInfo
from galang_utils.rigbuilder.modules.module_limb.constant.constant_module import *
from galang_utils.rigbuilder.modules.module_limb.base.controls import LimbControlCreator
from galang_utils.rigbuilder.modules.module_limb.base.jointchain import LimbJointChainSetup


class LimbIKComponent:
    def __init__(self, guide):
        self.guide = GuideInfo(guide)
        self.module = ModuleInfo(guide)
        self.ik_limb_map: Dict[GuideInfo, Dict[str, Union[LimbControlCreator, str]]] = {}
        self.ik_limb_group: str = None
        self.ik_moudle_handle: str = None

    def create(self):
        # Step 0: Create FK Module Group
        group_name = limb_level_format(PJ, IK, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.ik_limb_group = cmds.group(em=True, name=group_name)
            cmds.xform(self.ik_limb_group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # Step 1 : Create IK joint chain
        ik_joint_chain = LimbJointChainSetup(self.guide.name, IK)
        cmds.parent(ik_joint_chain.group, self.ik_limb_group)

        # Step 2 : Create IK controls
        limb_guides: List[GuideInfo] = self.module.guides + self.module.guides_end
        for index, guide_jnt in enumerate(limb_guides):
            if index == 1:
                guide_name = self.module.guides_pv[0].name
            else:
                guide_name = guide_jnt.name
            ik_control = LimbControlCreator(guide_name, IK, self.module.type)
            ik_control.create()

            # Step 3 : Map IK controls and joints
            ik_joint = ik_joint_chain.output.get(guide_jnt.name)
            self.ik_limb_map[guide_jnt] = {CTRL: ik_control, JNT: ik_joint}

        # Step 4 : Create IK handle
        ik_handle_name = limb_level_format(PJ, IK, self.guide.side, self.guide.name_raw, level=None)
        ik_solver_name = limb_level_format(PJ, IK, self.guide.side, self.guide.name_raw, level=None, item="RPsolver")
        self.ik_moudle_handle = cmds.ikHandle(
            n=ik_handle_name,
            sj=self.ik_limb_map[self.module.guides[0][JNT]],
            ee=self.ik_limb_map[self.module.guides[2][JNT]],
            sol="ikRPsolver",
        )[0]
        cmds.rename("effector1", ik_solver_name)
        cmds.parent(self.ik_moudle_handle, self.ik_limb_map[self.module.guides[2]][CTRL].ctrl)
