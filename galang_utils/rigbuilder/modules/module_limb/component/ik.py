from maya import cmds
from typing import Dict, Union
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
        self.map: Dict[GuideInfo, Dict[str, Union[LimbControlCreator, str]]] = {}
        self.group: str = None
        self.handle: str = None

    def create(self):
        # Step 0: Create FK Module Group
        group_name = limb_level_format(PJ, IK, self.guide.side, self.guide.name_raw, GROUP)
        if not cmds.objExists(group_name):
            self.group = cmds.group(em=True, name=group_name)
            cmds.xform(self.group, t=self.guide.position, ro=self.guide.orientation)
        else:
            cmds.warning(f"you've already made {group_name}. Skipppppz")

        # Step 1 : Create IK joint chain
        ik_joint_chain = LimbJointChainSetup(self.guide.name, IK)
        ik_joint_chain.build()
        cmds.parent(ik_joint_chain.group, self.group)

        # Step 2 : Create IK controls
        for index, guide_jnt in enumerate(self.module.guides + self.module.guides_end):
            if index == 1:
                guide_obj = self.module.guides_pv[0]
            else:
                guide_obj = guide_jnt
            ik_control = LimbControlCreator(guide_obj, IK, self.module)
            ik_control.create()
            cmds.parent(ik_control.top, self.group)

            # Step 3 : Map IK controls and joints
            ik_joint = ik_joint_chain.output.get(guide_jnt.name)
            self.map[guide_jnt.name] = {CTRL: ik_control, JNT: ik_joint}

        # Step 4 : Create IK handle
        ik_handle_name = limb_level_format(PJ, IK, self.guide.side, self.guide.name_raw, level=None)
        ik_solver_name = limb_level_format(PJ, IK, self.guide.side, self.guide.name_raw, level=None, item="RPsolver")
        self.handle = cmds.ikHandle(
            n=ik_handle_name,
            sj=self.map[self.module.guides[0].name][JNT],
            ee=self.map[self.module.guides_end[0].name][JNT],
            sol="ikRPsolver",
        )[0]
        cmds.rename("effector1", ik_solver_name)
        cmds.parent(self.handle, self.map[self.module.guides_end[0].name][CTRL].ctrl)
        cmds.poleVectorConstraint(self.map[self.module.guides[1].name][CTRL].ctrl, self.handle)
